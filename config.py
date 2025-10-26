import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

IMAGES_DIR = "images/horror"
QUEST_FILE = "horror_quests.json"
