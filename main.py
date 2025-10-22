from telegram import ApplicationBuilder
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from handlers import runa, symbol, mist, gif, path_game, other_handlers

# Чтение токена из переменных окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков команд
    app.add_handler(CommandHandler("runa", runa.runa))
    app.add_handler(CommandHandler("symbol", symbol.symbol))
    app.add_handler(CommandHandler("mist", mist.mist))
    app.add_handler(CommandHandler("gif", gif.send_gif))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, other_handlers.quest_trigger))
    path_game.register(app)

    # Начинаем прослушивание входящих сообщений
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())