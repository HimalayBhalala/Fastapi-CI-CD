from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

print("DATABASE_PORT:", os.getenv("DATABASE_PORT"))
print("ACCESS_TOKEN_EXPIRE_MINUTES:", os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class AllSettings(BaseSettings):
    database_username: str
    database_name: str
    database_password: str
    database_port: str
    database_hostname: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = AllSettings()
