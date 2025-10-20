from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, MessageHandler, filters, CallbackContext,
    CallbackQueryHandler, CommandHandler
)
import os
import json

# 🔸 Токен бота берём из переменной окружения
TOKEN = os.environ.get("TOKEN")  # ← В Render создаём ENV с именем TOKEN и значением токена
# 🔹 Папка с артом
ARTS_DIR = "assets"

# 🔸 Квесты
QUESTS = {
    "светлая долина": os.path.join(ARTS_DIR, "Light valley"),
    "тёмный лес": os.path.join(ARTS_DIR, "Темный лес"),
    "испытание завесы": os.path.join(ARTS_DIR, "The test of the veil")
}

# 🔹 Руны
RUNES_DIR = os.path.join(ARTS_DIR, "runy")

# === Получение файлов из папки квеста
def get_arts(quest_name):
    path = QUESTS.get(quest_name, "")
    if not os.path.exists(path):
        return []
    return [os.path.join(path, f) for f in os.listdir(path)
            if f.lower().endswith((".png", ".jpg", ".gif", ".webp"))]

# === Получение файлов рун
def get_runes():
    if not os.path.exists(RUNES_DIR):
        return []
    return [os.path.join(RUNES_DIR, f) for f in os.listdir(RUNES_DIR)
            if f.lower().endswith((".png", ".jpg", ".gif", ".webp"))]

# === Приветствие
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🌞 Светлая Долина", callback_data="quest_light")],
        [InlineKeyboardButton("🌲 Тёмный Лес", callback_data="quest_dark")],
        [InlineKeyboardButton("⚜ Испытание Завесы", callback_data="quest_veil")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "✨ Добро пожаловать в мир NOSTAI!\nВыбери свой путь:",
        reply_markup=reply_markup
    )

# === Обработка кнопок приветствия
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "quest_light":
        await start_quest(query, context, "светлая долина")
    elif query.data == "quest_dark":
        await start_quest(query, context, "тёмный лес")
    elif query.data == "quest_veil":
        # Фракционный квест с подтверждением
        keyboard = [
            [InlineKeyboardButton("🔮 Войти в Завесу", callback_data="enter_veil")],
            [InlineKeyboardButton("⚖️ Отступить", callback_data="decline_veil")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🌒 Завеса шевелится...\n🕯 Нить реальности истончается...\nТы можешь:",
            reply_markup=reply_markup
        )
    elif query.data == "enter_veil":
        await query.edit_message_text("🕯 Завеса раскрывается... ритуал начинается...")
        await start_quest(query, context, "испытание завесы")
    elif query.data == "decline_veil":
        await query.edit_message_text("⚖️ Завеса остаётся закрытой... пока что.")

# === Запуск квеста
async def start_quest(update_or_query, context: CallbackContext, quest_name):
    if hasattr(update_or_query, "message"):
        chat = update_or_query.effective_chat
    else:
        chat = update_or_query.message.chat

    # Создаём отдельную комнату/топик (если поддерживается)
    try:
        thread = await context.bot.create_forum_topic(chat_id=chat.id, name=f"🌀 {quest_name.title()}")
        thread_id = thread.message_thread_id
    except Exception:
        thread_id = None

    # Отправка артов квеста
    arts = get_arts(quest_name)
    if arts:
        media_group = [InputMediaPhoto(open(a, "rb")) for a in arts]
        if thread_id:
            await context.bot.send_media_group(chat_id=chat.id, media=media_group, message_thread_id=thread_id)
        else:
            await context.bot.send_media_group(chat_id=chat.id, media=media_group)

    # Отправка текста-завязки
    if quest_name == "светлая долина":
        text = "☀️ Ты входишь в долину света. Воздух пахнет пеплом и мёдом, но под кожей чувствуешь тревогу..."
    elif quest_name == "тёмный лес":
        text = "🌑 В лесу темно, как в утробе Земли. Ветви словно когти, а дыхание становится тяжелее..."
    else:
        text = "🕯 Завеса зовёт... фракции вступают в ритуал, и реальность колеблется."

    await context.bot.send_message(chat_id=chat.id, text=text, message_thread_id=thread_id)

    # Отправка рун
    runes = get_runes()
    if runes:
        media_group = [InputMediaPhoto(open(r, "rb")) for r in runes]
        await context.bot.send_media_group(chat_id=chat.id, media=media_group, message_thread_id=thread_id)

# === Основная функция
def main():
    print("⚡ Бот запускается...")
    app = ApplicationBuilder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    # Обработка кнопок
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Бот запущен! Ждём сообщений...")
    app.run_polling()

if __name__ == "__main__":
    main()

