import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    DATABASE_ALEMBIC_URL = os.getenv("DATABASE_ALEMBIC_URL")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    B2_KEY_ID: str = os.getenv("B2_KEY_ID")
    B2_APP_KEY: str = os.getenv("B2_APP_KEY")
    BUCKET_ID: str = os.getenv("BUCKET_ID")
    BUCKET_NAME: str= os.getenv("BUCKET_NAME")
    
settings = Settings()
