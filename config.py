import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, 'assets', 'General')
IMAGES_DIR = os.path.join(BASE_DIR, 'assets', 'Images')
QUEST_FILE = os.path.join(BASE_DIR, 'quests.json')
