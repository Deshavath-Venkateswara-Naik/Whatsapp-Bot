import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PICKY_API_KEY = os.getenv("PICKY_API_KEY")
    PICKY_DEVICE_ID = os.getenv("PICKY_DEVICE_ID")

settings = Settings()