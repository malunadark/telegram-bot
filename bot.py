import os
import logging
from telegram.ext import ApplicationBuilder

from handlers.quests import quest_handler
from handlers.welcome import welcome_handler
from handlers.topics import topic_handler

logging.basicConfig(level=logging.INFO)

def create_app():
    TOKEN = os.getenv("BOT_TOKEN")  # ⚡ самое важное

    if not TOKEN:
        raise ValueError("❌ BOT_TOKEN не найден! Добавь его в Render → Environment.")

    app = ApplicationBuilder().token(8296279646:AAG1OrvQlbQgri3WZwiivQ0ylHYrECxHLBY).build()

    app.add_handler(quest_handler)
    app.add_handler(welcome_handler)
    app.add_handler(topic_handler)

    return app

