from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # read all variables from .env file
    COSMOS_CONNECTION_STRING = os.getenv("COSMOS_CONNECTION_STRING")
    COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
    COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME")
    BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
    BLOB_ENDPOINT = os.getenv("BLOB_ENDPOINT")
    

settings = Settings()