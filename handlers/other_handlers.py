from telegram import Update
from telegram.ext import ContextTypes

async def new_user_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"🌟 Добро пожаловать, {user.first_name}! Тебя ждут великие приключения.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        raise context.error
    except Exception as e:
        print(f"Ошибка: {e}")
