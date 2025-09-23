import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 🔑 Токен берём из переменной окружения Render
TOKEN = os.environ['TELEGRAM_TOKEN']

# Путь к видео (относительно корня проекта)
VIDEO_PATH = "assets/general/Rune.mp4"

# 📌 Команда /background — отправка видео
async def send_background(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(VIDEO_PATH):
        await update.message.reply_text("❌ Видео не найдено!")
        return
    with open(VIDEO_PATH, "rb") as video:
        await update.message.reply_video(video, caption="✦ Фоновое видео Rune")

def main():
    app = Application.builder().token(TOKEN).build()

    # Команда /background
    app.add_handler(CommandHandler("background", send_background))

    print("Бот запущен! Ждём команд...")
    app.run_polling()

if __name__ == "__main__":
    main()

