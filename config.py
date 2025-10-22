import os
from dotenv import load_dotenv

# Загрузим переменные окружения из .env
load_dotenv()

# Базовые настройки
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'General')  # Пути к активам
GIF_PATH = os.path.join(ASSETS_DIR, 'Rune.gif')