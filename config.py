from pydantic import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    AUTH_TOKEN: str = os.getenv("AUTH_TOKEN", "defaulttoken")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_CACHE_TIMEOUT: int = int(os.getenv("REDIS_CACHE_TIMEOUT", 300))

settings = Settings()
