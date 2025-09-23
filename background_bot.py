import os
from telegram import InputMediaAnimation, InputMediaPhoto
from telegram.ext import CommandHandler, ContextTypes, Application

ASSETS_DIR = "assets"
GENERAL_DIR = os.path.join(ASSETS_DIR, "general")

# 📌 /background — отправляет GIF как фон
async def background(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gif_path = os.path.join(GENERAL_DIR, "rune.mp4")  # Имя твоего GIF
    if not os.path.exists(gif_path):
        await update.message.reply_text("❌ Фон не найден.")
        return
    
    # Отправляем GIF
    await update.message.reply_animation(open(gif_path, "rb"), caption="🌑 Фон загружен!")

# 📌 /overlay — отправляет картинку поверх фона (имитация)
async def overlay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Здесь можно выбирать случайное изображение из папки runes
    runes_dir = os.path.join(ASSETS_DIR, "runes")
    if not os.path.exists(runes_dir):
        await update.message.reply_text("❌ Папка runes пуста или не найдена.")
        return
    rune = random.choice(os.listdir(runes_dir))
    with open(os.path.join(runes_dir, rune), "rb") as photo:
        await update.message.reply_photo(photo, caption="✦ Руна на фоне...")

# В main() добавляем команды
app.add_handler(CommandHandler("background", background))
app.add_handler(CommandHandler("overlay", overlay))
