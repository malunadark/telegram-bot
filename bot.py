import logging
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters
from handlers.path_game import start_horror_quest, horror_button_handler
from handlers.other_handlers import greet_new_user
from config import TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO  # INFO и выше будет отображаться
)
logger = logging.getLogger(__name__)

def create_bot():
    """
    Создаёт и настраивает экземпляр Telegram бота.
    """
    app = ApplicationBuilder().token(TOKEN).build()

    # Приветствие новых пользователей
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_user))

    # Запуск квеста
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start_horror_quest))

    # Обработка выбора в квесте
    app.add_handler(CallbackQueryHandler(horror_button_handler))

    return app


def run_bot():
    """
    Запускает бота с логированием.
    """
    app = create_bot()
    logger.info("🔥 Bot запущен и ждёт сигнал из Тумана...")
    try:
        app.run_polling()
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")


if __name__ == "__main__":
    run_bot()
