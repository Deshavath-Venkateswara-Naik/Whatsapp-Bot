import httpx
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger()

async def send_message(to: str, message: str):
    # 🚀 Direct API v2: Structure provided by user
    url = "https://app.pickyassist.com/api/v2/push"

    # Ensure number format - keeping digits only for reliability
    clean_number = "".join(filter(str.isdigit, to))

    # User provided structure (Direct message, no template)
    payload = {
        "token": settings.PICKY_API_TOKEN,
        "application": settings.PICKY_APP_ID,
        "data": [
            {
                "number": clean_number,
                "message": message,
                "language": "en"
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Sending message to {to} matching user template structure")
            
            response = await client.post(url, json=payload, timeout=10)
            
            logger.info(f"Picky Assist HTTP Status: {response.status_code}")
            logger.info(f"Picky Assist Response Body: {response.text}")
            
            try:
                res_json = response.json()
            except Exception:
                if response.status_code in [200, 202]:
                    return {"status": 200, "message": "Success (Non-JSON response)"}
                return {"status": response.status_code, "message": "Invalid JSON response"}

            # If Direct API fails with 401, fallback to Connector or try a standard "message" field inside data
            if res_json.get("status") == 401:
                logger.warning("Direct API 401. Trying Connector Fallback...")
                connector_url = "https://app.pickyassist.com/url/9baf349ec6c561c85d6950671dd608995fed656d"
                fallback_payload = {"number": clean_number, "message": message, "reply": message}
                fallback_res = await client.post(connector_url, json=fallback_payload, timeout=5)
                if fallback_res.status_code == 200:
                    return {
                        "status": 200, 
                        "message": "Success (via Connector Fallback)",
                        "connector_log": fallback_res.headers.get("picky-connector-log")
                    }

            return res_json

        except Exception as e:
            logger.error(f"Error sending message to Picky Assist: {str(e)}")
            return {"error": str(e)}

async def forward_payload(payload: dict):
    # 🚀 Raw forwarding to Picky Assist Direct API v2
    url = "https://app.pickyassist.com/api/v2/push"
    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Forwarding raw payload to Picky Assist")
            response = await client.post(url, json=payload, timeout=10)
            logger.info(f"Forward result: {response.status_code}")
            
            # Picky Assist often sends JSON but with text/html header
            try:
                return response.json()
            except Exception:
                return {"status": response.status_code, "text": response.text}
                
        except Exception as e:
            logger.error(f"Error forwarding payload: {str(e)}")
            return {"error": str(e)}