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
    def validate(cls):
        # Custom validation method to debug values
        database_port = os.getenv("DATABASE_PORT")
        access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

        try:
            int(database_port)
        except (TypeError, ValueError):
            print(f"Invalid value for DATABASE_PORT: {database_port}")
        
        try:
            int(access_token_expire_minutes)
        except (TypeError, ValueError):
            print(f"Invalid value for ACCESS_TOKEN_EXPIRE_MINUTES: {access_token_expire_minutes}")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


# Instantiate the settings object
settings = AllSettings()
settings.validate()
