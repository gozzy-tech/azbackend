from pydantic import computed_field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):

    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "postgresql+asyncpg://postgres:Sirnduu1@localhost:5432/azdatabase")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://default:Sirnduu1@localhost:6379/0")
    FLOWER_BASIC_AUTH: str = os.getenv("FLOWER_BASIC_AUTH", "admin:admin")

    # App settings
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "GozzyTech API Service")
    SERVICE_URL: str = os.getenv("SERVICE_URL", "http://localhost:8000")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    VERSION: str = os.getenv("VERSION", "1.0.0")

    # Auth Settings
    JWT_SECRET: str = os.getenv("JWT_SECRET", "secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRY: int = int(os.getenv("ACCESS_TOKEN_EXPIRY", 172800))
    REFRESH_TOKEN_EXPIRY: int = int(os.getenv("REFRESH_TOKEN_EXPIRY", 604800))

    # Brevo Settings
    BREVO_API_KEY: str = os.getenv("BREVO_API_KEY", "your-brevo-api-key")
    BREVO_SMS_SENDER: str = os.getenv("BREVO_SMS_SENDER", "your-sms-sender")

    # Paystack Settings
    PAYSTACK_SECRET_KEY: str = os.getenv("PAYSTACK_SECRET_KEY", "your-paystack-secret-key")
    PAYSTACK_PUBLIC_KEY: str = os.getenv("PAYSTACK_PUBLIC_KEY", "your-paystack-public-key")

    @computed_field
    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.REDIS_URL

    class Config:
        env_file = ".env"  # Load from .env file
        env_file_encoding = "utf-8"


# Create an instance of settings
settings = Settings()
