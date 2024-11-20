from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv() 
class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    GEMINI_KEY: str = os.getenv("GEMINI_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 55  
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

settings = Settings()
