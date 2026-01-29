from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    FIREBASE_PROJECT_ID: str
    FIREBASE_CLIENT_EMAIL: Optional[str] = None
    FIREBASE_PRIVATE_KEY: Optional[str] = None
    
    JWT_SECRET_KEY: str = "your-secret"
    JWT_ALGORITHM: str = "HS256"
    ENVIRONMENT: str = "development"

    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }

settings = Settings()
