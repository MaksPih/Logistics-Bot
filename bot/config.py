from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")