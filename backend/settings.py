from dotenv import load_dotenv
import os

load_dotenv()
KONTAKT_API_KEY = os.getenv("KONTAKT_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL") + "?sslmode=require"