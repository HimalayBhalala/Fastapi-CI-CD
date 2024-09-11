from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class AllSettings(BaseSettings):
    database_username: str
    database_name: str
    database_password: str
    database_port: int
    database_hostname: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    @classmethod
    def __init_subclass__(cls):
        # Convert environment variables to the expected types
        cls.database_port = int(os.getenv("DATABASE_PORT", 5432))
        cls.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = AllSettings()
