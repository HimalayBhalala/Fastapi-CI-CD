# config.py
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

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = AllSettings()
