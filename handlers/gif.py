from telegram import Update
from telegram.ext import ContextTypes
from config import GIF_PATH

async def send_gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(GIF_PATH):
        await update.message.reply_text("❌ Гифка не найдена!")
        return
    with open(GIF_PATH, "rb") as f:
        await update.message.reply_animation(f, caption="✦ Магическая руна пробуждается...")
