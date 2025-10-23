from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, MessageHandler, filters, CallbackContext,
    CallbackQueryHandler
)
from dotenv import load_dotenv
import os
import random
import json

# 🔹 Загружаем переменные окружения из .env
load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")

# 🔹 Папка с изображениями (например, images/horror)
IMAGES_DIR = "images/horror"

# 🔹 Загружаем квесты
with open("horror_quests.json", encoding="utf-8") as f:
    QUESTS_DATA = json.load(f).get("quests", {})

# 🔹 Функция для получения случайного изображения
def get_random_image():
    images = os.listdir(IMAGES_DIR)
    if images:
        return os.path.join(IMAGES_DIR, random.choice(images))
    return None

# 🔹 Приветственное сообщение при входе пользователя
async def greet_new_user(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_text(f"Здравствуй Придший, {user.first_name}! Загляни за грань реальности, пробуди вечность из глубины веков, отступать нельзя впереди туманый пожар, берегись его он повсюду.")
# 🔹 Запуск квеста
async def start_horror_quest(update: Update, context: CallbackContext):
    first_scene = QUESTS_DATA.get("first_scene", {})
    keyboard = [[InlineKeyboardButton(text, callback_data=cb)] for text, cb in first_scene.get("options", [])]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(first_scene.get("text", ""), reply_markup=reply_markup)

# 🔹 Обработка кликов на кнопки
async def horror_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    current_scene = QUESTS_DATA.get(query.data, {})
    text = current_scene.get("text", "")
    options = current_scene.get("options", [])
    image = None

    # Каждые два кадра показываем картинку
    if len(options) % 2 != 0:
        image = get_random_image()

    # Формируем клавиатуру и отправляем
    keyboard = [[InlineKeyboardButton(text, callback_data=cb)] for text, cb in options]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if image:
        await query.edit_message_media(media=InputMediaPhoto(open(image, "rb")))
        await query.edit_message_caption(caption=text, reply_markup=reply_markup)
    else:
        await query.edit_message_text(text, reply_markup=reply_markup)

# 🔹 Основная функция
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_user))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start_horror_quest))
    app.add_handler(CallbackQueryHandler(horror_button_handler))

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
