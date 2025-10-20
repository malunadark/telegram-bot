from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, MessageHandler, filters, CallbackContext,
    CallbackQueryHandler
)
import os
import json

# 🔸 Токен бота (замени на свой токен)
TOKEN = "BOT_TOKEN"

# 🔹 Путь к папке с артами
ARTS_DIR = "assets"

# 🔸 Загружаем квесты из JSON
with open("quests.json", encoding="utf-8") as f:
    QUESTS_DATA = json.load(f)["quests"]

# === Получение артов квеста
def get_arts(quest_name):
    path = QUESTS_DATA[quest_name]["folder"]
    if not os.path.exists(path):
        return []
    files = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.lower().endswith((".jpg", ".png", ".webp", ".gif"))
    ]
    return files

# === Обработка текстовых сообщений для запуска квестов
async def quest_trigger(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    for quest_name, quest in QUESTS_DATA.items():
        if any(word.lower() in text for word in quest["trigger_words"]):
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
    if data.startswith("enter_"):
        quest_name = data.replace("enter_", "")
        quest = QUESTS_DATA[quest_name]
        await query.edit_message_text(quest["on_accept"])
        await start_quest(query, context, quest_name)
    elif data.startswith("decline_"):
        quest_name = data.replace("decline_", "")
        await query.edit_message_text(f"⚖️ {QUESTS_DATA[quest_name]['confirmation_text']} отменено.")

# === Запуск квеста и отправка артов
async def start_quest(update_or_query, context: CallbackContext, quest_name):
    if hasattr(update_or_query, "message"):
        chat_id = update_or_query.effective_chat.id
    else:
        chat_id = update_or_query.message.chat.id

    quest = QUESTS_DATA[quest_name]

    # Создаём комнату/топик (если поддерживается)
    try:
        thread = await context.bot.create_forum_topic(
            chat_id=chat_id, name=quest["room_name"]
        )
        thread_id = thread.message_thread_id
    except Exception:
        thread_id = None

    # Отправка артов
    arts = get_arts(quest_name)
    media_group = [InputMediaPhoto(open(a, "rb")) for a in arts]
    if media_group:
        if thread_id:
            await context.bot.send_media_group(chat_id=chat_id, media=media_group, message_thread_id=thread_id)
        else:
            await context.bot.send_media_group(chat_id=chat_id, media=media_group)

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


