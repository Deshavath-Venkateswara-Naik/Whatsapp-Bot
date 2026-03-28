import asyncio
from app.services.picky_service import send_message

async def test_send():
    # 🚀 Testing with the actual service implementation
    to = "919000000000"  # Replace with a real number for manual test
    message = "Test message from WhatsApp Bot (Picky Assist Connector)"

    try:
        print(f"Sending message to {to} via Picky Assist...")
        result = await send_message(to, message)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_send())
