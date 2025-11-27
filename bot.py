import logging
from telegram.ext import ApplicationBuilder

from config import TOKEN
from handlers.quests import quest_handler
from handlers.welcome import welcome_handler
from handlers.topics import topic_handler

logging.basicConfig(level=logging.INFO)

def create_app():
    app = ApplicationBuilder().token(TOKEN).build()

    # Квесты
    app.add_handler(quest_handler)

    # Приветствие
    app.add_handler(welcome_handler)

    # Создание тем
    app.add_handler(topic_handler)

    return app
