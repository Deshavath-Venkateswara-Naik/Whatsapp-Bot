from fastapi import FastAPI, Request
import httpx
import traceback
from app.services.openai_service import get_ai_response
from app.services.picky_service import send_message, forward_payload
from app.utils.logger import get_logger
import urllib.parse


app = FastAPI()
logger = get_logger()

@app.get("/")
def home():
    return {"status": "Bot is running"}

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        logger.info(f"Incoming Webhook Data: {data}")

        # 🔍 Robust extraction of message and sender
        user_message = (
            data.get("message_in_raw") or 
            data.get("message-in") or 
            data.get("message") or 
            data.get("text")
        )
        sender = (
            data.get("number") or 
            data.get("from") or 
            data.get("sender")
        )

        if not user_message:
            logger.warning(f"No message found in data: {data}")
            return {"status": "no message"}
        
        if not sender:
            logger.error(f"No sender number found in data: {data}")
            return {"status": "no sender"}

        # 🔧 Fix URL encoding
        user_message = urllib.parse.unquote_plus(user_message)

        # 🤖 Get AI response
        logger.info(f"Processing message from {sender}: {user_message}")
        ai_reply = get_ai_response(user_message)
        
        # 🧪 Handle AI Errors (Quota etc) by sending a fallback message
        if ai_reply.startswith("OpenAI Error") or ai_reply.startswith("Error:"):
            logger.warning(f"AI Failed, sending fallback: {ai_reply}")
            ai_reply = "Hi! I'm sorry, I'm currently experiencing some technical issues. Please try again later or visit www.turito.com for assistance."

        logger.info(f"Final Reply for {sender}: {ai_reply}")

        # 📤 Automating the call to local api/v2/push as requested
        # We construct the JSON and send it to our own local endpoint
        from app.config import settings
        picky_payload = {
            "token": settings.PICKY_API_TOKEN,
            "application": settings.PICKY_APP_ID,
            "data": [
                {
                    "number": sender,
                    "message": ai_reply,
                    "language": "en"
                }
            ]
        }

        async with httpx.AsyncClient() as client:
            try:
                # 🚀 Calling the local endpoint automatically
                local_url = "http://127.0.0.1:8000/api/v2/push"
                logger.info(f"Automatically triggering local API push for {sender}")
                response = await client.post(local_url, json=picky_payload, timeout=5)
                result = response.json()
                
                # 🔗 Fallback to Connector if the local push (which forwards to Direct API) returns 401
                if result.get("status") == 401 or (isinstance(result.get("text"), str) and "401" in result.get("text")):
                    logger.warning(f"Direct API 401 detected in local push. Trying Connector fallback...")
                    fallback_result = await send_message(sender, ai_reply)
                    logger.info(f"Connector Fallback result: {fallback_result}")
                    return {"status": "success", "method": "connector_fallback", "ai_response": ai_reply}
                
                return {"status": "success", "ai_response": ai_reply, "api_result": result}
            except Exception as e:
                logger.error(f"Error calling local API: {str(e)}")
                # Direct fallback if anything goes wrong
                return await send_message(sender, ai_reply)

    except Exception as e:
        logger.error(f"Critical error in webhook: {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/api/v2/push")
async def picky_api_push(request: Request):
    try:
        data = await request.json()
        logger.info(f"Incoming API Push Data: {data}")
        # 🚀 Forward to real Picky Assist API
        result = await forward_payload(data)
        logger.info(f"Forward result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in local proxy: {str(e)}")
        return {"error": str(e)}


def extract_message(data: dict):
    try:
        return (
            data.get("message_in_raw") or 
            data.get("message-in") or 
            data.get("message") or 
            data.get("text")
        )
    except Exception:
        return None


def extract_sender(data: dict):
    """
    Extracts the sender's number from various potential payload formats.
    """
    try:
        return (
            data.get("number") or 
            data.get("from") or 
            data.get("sender")
        )
    except Exception:
        return None