from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
MEDIUM_EMAIL = os.getenv("MEDIUM_EMAIL")
MEDIUM_PASSWORD = os.getenv("MEDIUM_PASSWORD")