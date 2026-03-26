import httpx
from app.utils.logger import get_logger

logger = get_logger()

async def send_message(to: str, message: str):
    # 🚀 FINAL FIX: Using specific Channel URL provided by user
    url = "https://app.pickyassist.com/url/591be9e9f1c749d822bfe3bd3c55256b508aedf4"


    payload = {
        "reply": message,
        "number": to
    }



    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Sending message to {to} via Picky Assist Channel URL")
            
            response = await client.post(url, json=payload, timeout=10)
            
            logger.info(f"Picky Assist HTTP Status: {response.status_code}")
            logger.info(f"Picky Assist Response Body: {response.text}")
            
            # 🔍 Safely handle JSON parsing (in case of empty/non-JSON response)
            try:
                res_json = response.json()
            except Exception:
                # If it's not JSON but status is 200/202, it's a success
                if response.status_code in [200, 202]:
                    return {"status": 200, "message": "Success (Non-JSON response)"}
                return {"status": response.status_code, "message": "Invalid JSON response"}

            if res_json.get("status") not in [200, 202]:
                logger.warning(f"Picky Assist API Warning: {res_json.get('message')}")
                
            return res_json


        except Exception as e:
            logger.error(f"Error sending message to Picky Assist: {str(e)}")
            return {"error": str(e)}