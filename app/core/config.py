from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "databaseUrl" 
    SECRET_KEY: str = "secretKey" 
    ALGORITHM: str = "algorithm" 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 55  
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

settings = Settings()
