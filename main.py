import os
import random
import json
from dotenv import load_dotenv
from telegram import (
    Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

# 🔹 Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "8443"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

# 🔹 Папка с изображениями
IMAGES_DIR = "images/horror"

# 🔹 Загружаем квесты
with open("horror_quests.json", encoding="utf-8") as f:
    QUESTS_DATA = json.load(f).get("quests", {})

# 🔹 Состояние пользователей
USER_STATE = {}

# -----------------------------
# Приветствие при входе в чат
# -----------------------------
async def greet_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Здравствуй, Придший {user.first_name or 'странник'}...\n\n"
        "Загляни за грань реальности, пробуди вечность из глубины веков.\n"
        "Отступать нельзя — впереди туманный пожар. Берегись его... он повсюду."
    )

# -----------------------------
# Команда /start
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_scene = QUESTS_DATA.get("first_scene", {})
    USER_STATE[update.effective_user.id] = "first_scene"

    keyboard = [
        [InlineKeyboardButton(text, callback_data=cb)] for text, cb in first_scene.get("options", [])
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(first_scene.get("text", ""), reply_markup=reply_markup)

# -----------------------------
# Отправка сцены
# -----------------------------
async def send_scene(update: Update, context: ContextTypes.DEFAULT_TYPE, scene_id: str):
    scene = QUESTS_DATA.get(scene_id, {})
    text = scene.get("text", "")
    options = scene.get("options", [])
    image_file = scene.get("image")

    keyboard = [[InlineKeyboardButton(text, callback_data=cb)] for text, cb in options]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Показ картинки, если есть
    if image_file and os.path.exists(os.path.join(IMAGES_DIR, image_file)):
        with open(os.path.join(IMAGES_DIR, image_file), "rb") as img:
            await update.callback_query.message.edit_media(
                media=InputMediaPhoto(img, caption=text),
                reply_markup=reply_markup
            )
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

# -----------------------------
# Обработка кнопок
# -----------------------------
async def horror_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    current_scene_id = USER_STATE.get(user_id, "first_scene")
    next_scene_id = query.data

    if next_scene_id not in QUESTS_DATA:
        await query.edit_message_text("🔥 Конец пути. Всё тонет в пепле и тумане...")
        return

    USER_STATE[user_id] = next_scene_id
    await send_scene(update, context, next_scene_id)

# -----------------------------
# Основная функция
# -----------------------------
def main():
    app = Application.builder().token(TOKEN).build()

    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_user))
    app.add_handler(CallbackQueryHandler(horror_button_handler))

    # Render webhook
    if WEBHOOK_URL:
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path="",
            webhook_url=WEBHOOK_URL
        )
    else:
        app.run_polling()

if __name__ == "__main__":
    main()
