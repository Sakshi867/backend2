from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/daysense"
    FIREBASE_PROJECT_ID: str
    JWT_AUDIENCE: str
    ENVIRONMENT: str = "development"
    
    # Secret key for local testing if needed, though we use Firebase
    SECRET_KEY: str = "your-secret-key"

    class Config:
        env_file = ".env"

settings = Settings()
