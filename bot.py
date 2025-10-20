import os
import json
import logging
from telegram import (
    Update,
    InputMediaPhoto,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Загрузка квестов ===
with open("quests.json", "r", encoding="utf-8") as f:
    QUESTS = json.load(f)["quests"]

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("❌ BOT_TOKEN не найден! Добавь его в Render → Environment → BOT_TOKEN")

# Активные квесты: user_id → quest_name
active_quests = {}

# Пошаговые сцены: user_id → текущий шаг
quest_progress = {}

# === Приветствие ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"🌒 Привет, {user.first_name}.\n\n"
        "Ты вошёл в мир **NOSTAI**.\n"
        "🕯 Здесь Завеса между мирами истончена.\n\n"
        "Чтобы начать путь, напиши одно из слов:\n"
        "— `пепел`\n— `долина`\n— `лес`\n— `завеса`\n\n"
        "Завеса ждёт..."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# === Обработка сообщений ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()

    # Проверяем, если игрок внутри квеста и пишет "продолжить"
    if user_id in active_quests and text == "продолжить":
        await continue_quest(update, context)
        return

    # Проверяем триггерные слова
    for quest_name, quest in QUESTS.items():
        for trigger in quest["trigger_words"]:
            if trigger in text:
                await send_intro(update, quest_name, quest)
                return

    await update.message.reply_text("🌫 Завеса не слышит тебя... Попробуй другое слово.")

# === Отправка вступления квеста ===
async def send_intro(update: Update, quest_name, quest):
    keyboard = [
        [InlineKeyboardButton("🔮 Войти", callback_data=f"accept_{quest_name}")],
        [InlineKeyboardButton("⚖️ Отступить", callback_data="decline")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(quest["intro_text"], reply_markup=markup)

# === Обработка кнопок ===
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data.startswith("accept_"):
        quest_name = query.data.replace("accept_", "")
        quest = QUESTS[quest_name]
        active_quests[user_id] = quest_name
        quest_progress[user_id] = 0  # первый шаг

        await query.message.reply_text(quest["on_accept"])
        await send_room_intro(query, quest)
    elif query.data == "decline":
        await query.message.reply_text("🌫 Завеса отступает. Возможно, позже...")

# === Вступление в комнату квеста ===
async def send_room_intro(update_or_query, quest):
    if hasattr(update_or_query, "message"):
        chat_id = update_or_query.message.chat.id
    else:
        chat_id = update_or_query.message.chat.id

    await update_or_query.message.reply_text(
        f"🏕 {quest['room_name']}\n{quest['room_description']}\n\n"
        "📜 Напиши `продолжить`, чтобы начать сцену."
    )

# === Пошаговое прохождение квеста ===
async def continue_quest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    quest_name = active_quests[user_id]
    quest = QUESTS[quest_name]

    # Получаем список артов
    arts = [f for f in os.listdir(quest["folder"]) if f.lower().endswith((".jpg", ".png", ".gif"))]
    arts.sort()  # последовательность по имени

    step = quest_progress[user_id]

    if step < len(arts):
        art_path = os.path.join(quest["folder"], arts[step])
        with open(art_path, "rb") as f:
            await update.message.reply_photo(f)

        # Можно добавить текст для каждого шага (пока используем intro_text)
        await update.message.reply_text(f"*Сцена {step + 1}:* {quest['intro_text']}", parse_mode="Markdown")
        quest_progress[user_id] += 1
    else:
        await update.message.reply_text("✨ Квест завершён. Ты можешь начать снова, написав ключевое слово.")
        del active_quests[user_id]
        del quest_progress[user_id]

# === Проверка активных квестов ===
async def rooms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in active_quests:
        quest_name = active_quests[user_id]
        quest = QUESTS[quest_name]
        await update.message.reply_text(
            f"🔮 Ты находишься в квесте: *{quest_name}*\n"
            f"📜 Комната: {quest['room_name']}",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("🌒 Ты пока не в Завесе... Напиши одно из слов: пепел, лес, долина, завеса.")

# === Запуск бота ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rooms", rooms))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_button))

    logger.info("🚀 Бот запущен и готов.")
    app.run_polling()

if __name__ == "__main__":
    main()
