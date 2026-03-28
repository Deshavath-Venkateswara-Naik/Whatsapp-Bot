import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PICKY_API_TOKEN = os.getenv("PICKY_API_TOKEN")
    PICKY_APP_ID = int(os.getenv("PICKY_APP_ID", 0))

settings = Settings()