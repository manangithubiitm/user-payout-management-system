from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

class Settings:
    MONGODB_URI = os.getenv("MONGODB_URI")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

settings  = Settings()