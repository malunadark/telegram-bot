import os
import json
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, MessageHandler, filters, CallbackContext,
    CallbackQueryHandler
)
from dotenv import load_dotenv

# 🔹 Загружаем переменные окружения из .env
load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

if not TOKEN:
    raise ValueError("⚠️ BOT_TOKEN не установлен в переменных окружения")
if ADMIN_CHAT_ID:
    ADMIN_CHAT_ID = int(ADMIN_CHAT_ID)

# 🔹 Папка с ассетами
ARTS_DIR = "assets"

# 🔹 Загружаем квесты
with open("quests.json", encoding="utf-8") as f:
    QUESTS_DATA = json.load(f).get("quests", {})

# === Получение артов квеста
def get_arts(quest_name):
    path = QUESTS_DATA.get(quest_name, {}).get("folder", "")
    if not os.path.exists(path):
        return []
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.lower().endswith((".jpg", ".png", ".webp", ".gif"))
    ]

# === Обработка текстовых сообщений для запуска квестов
async def quest_trigger(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    for quest_name, quest in QUESTS_DATA.items():
        triggers = quest.get("trigger_words", [])
        if any(word.lower() in text for word in triggers):
            if quest_name == "испытание завесы":
                await send_veil_invitation(update, quest_name)
            else:
                await start_quest(update, context, quest_name)
            break

# === Приглашение в Испытание Завесы с кнопками
async def send_veil_invitation(update: Update, quest_name):
    keyboard = [
        [InlineKeyboardButton("🔮 Войти в Завесу", callback_data=f"enter_{quest_name}")],
        [InlineKeyboardButton("⚖️ Отступить", callback_data=f"decline_{quest_name}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌒 Завеса шевелится...\n🕯 Нить реальности истончается...\nТы можешь:",
        reply_markup=reply_markup
    )

# === Обработка нажатий на кнопки
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    data = query.data
    quest_name = data.split("_", 1)[1]
    quest = QUESTS_DATA.get(quest_name, {})

    if data.startswith("enter_"):
        await query.edit_message_text(quest.get("on_accept", "Ты вошёл в квест..."))
        await start_quest(query, context, quest_name)
    elif data.startswith("decline_"):
        await query.edit_message_text(f"⚖️ {quest.get('confirmation_text', 'Отменено.')}")

# === Запуск квеста и отправка артов
async def start_quest(update_or_query, context: CallbackContext, quest_name):
    chat_id = (
        update_or_query.effective_chat.id
        if hasattr(update_or_query, "message")
        else update_or_query.message.chat.id
    )

    quest = QUESTS_DATA.get(quest_name, {})

    # Создаём топик/комнату (если поддерживается)
    thread_id = None
    try:
        thread = await context.bot.create_forum_topic(chat_id=chat_id, name=quest.get("room_name", quest_name))
        thread_id = thread.message_thread_id
    except Exception:
        pass  # Форумы могут быть не доступны

    # Отправка артов
    arts = get_arts(quest_name)
    for i in range(0, len(arts), 10):
        media_group = []
        for a in arts[i:i+10]:
            try:
                with open(a, "rb") as f:
                    media_group.append(InputMediaPhoto(f.read()))
            except Exception as e:
                print(f"⚠️ Ошибка при открытии файла {a}: {e}")
        if media_group:
            await context.bot.send_media_group(chat_id=chat_id, media=media_group, message_thread_id=thread_id)

    # Текстовая завязка
    intro_text = quest.get("intro_text", "Квест начинается...")
    await context.bot.send_message(chat_id=chat_id, text=intro_text, message_thread_id=thread_id)

# === Основная функция
def main():
    print("⚡ Бот запускается...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, quest_trigger))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Бот запущен! Ждём сообщений...")
    app.run_polling()

if __name__ == "__main__":
    main()
