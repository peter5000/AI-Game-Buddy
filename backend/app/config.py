from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    """
    A class to manage application settings from environment variables.

    This class loads environment variables from a .env file and makes them
    available as attributes. It centralizes configuration management, making it
    easier to access settings throughout the application.
    """

    # read all variables from .env file
    COSMOS_CONNECTION_STRING = os.getenv("COSMOS_CONNECTION_STRING")
    COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
    COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME")
    BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
    BLOB_ENDPOINT = os.getenv("BLOB_ENDPOINT")
    APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv(
        "APPLICATIONINSIGHTS_CONNECTION_STRING"
    )
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
    REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
    ALGORITHM = os.getenv("ALGORITHM")

    # temp PETER
    OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
    REDIS_CONNECTION_URL = os.getenv("REDIS_CONNECTION_URL")

    # const variables
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token valid for 30 minutes
    REFRESH_TOKEN_EXPIRE_DAYS = 14  # Token valid for 14 days


settings = Settings()
