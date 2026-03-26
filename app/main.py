from fastapi import FastAPI, Request
import traceback
from app.services.openai_service import get_ai_response
from app.services.picky_service import send_message
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
        logger.info(f"Incoming Data: {data}")

        # 🔍 Robust extraction of message and sender
        user_message = extract_message(data)
        sender = extract_sender(data)

        if not user_message:
            return {"status": "no message"}

        # 🔧 Fix URL encoding
        user_message = urllib.parse.unquote_plus(user_message)


        # 🤖 Get AI response
        ai_reply = get_ai_response(user_message)
        logger.info(f"AI Response: {ai_reply}")


        # 📤 Send back to WhatsApp (Awaiting the async call)
        await send_message(sender, ai_reply)

        return {"status": "success"}

    except Exception as e:
        logger.error(f"Critical error in webhook: {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}


def extract_message(data: dict):
    try:
        return (
            data.get("message-in") or 
            data.get("message_in_raw") or 
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
        # Format 1: from
        # Format 2: number
        return data.get("from") or data.get("number")
    except Exception:
        return None