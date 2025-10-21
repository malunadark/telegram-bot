import os
import json
from typing import List, Union

from telegram import (
    Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
)
from telegram.ext import (
    ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, ContextTypes
)
from dotenv import load_dotenv

# 🔹 Load env
load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

if not TOKEN:
    raise ValueError("⚠️ BOT_TOKEN не установлен в переменных окружения")
if ADMIN_CHAT_ID:
    ADMIN_CHAT_ID = int(ADMIN_CHAT_ID)

# 🔹 Assets root
ARTS_DIR = "assets"

# 🔹 Load quests
with open("quests.json", encoding="utf-8") as f:
    QUESTS_DATA = json.load(f).get("quests", {})

# === Utilities

def get_arts(quest_name: str) -> List[str]:
    folder = QUESTS_DATA.get(quest_name, {}).get("folder", "")
    # Join with ARTS_DIR if folder is relative and not already absolute
    path = folder if os.path.isabs(folder) else os.path.join(ARTS_DIR, folder) if folder else ""
    if not path or not os.path.exists(path):
        return []
    return [
        os.path.join(path, f)
        for f in sorted(os.listdir(path))
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif"))
    ]

def message_chat_and_thread(update: Union[Update, object]):
    chat_id = None
    thread_id = None
    if isinstance(update, Update):
        if update.effective_chat:
            chat_id = update.effective_chat.id
        if update.effective_message:
            # For forum topics, Telegram attaches message_thread_id
            thread_id = getattr(update.effective_message, "message_thread_id", None)
    return chat_id, thread_id

# === Handlers

async def quest_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower()
    # Simple word-boundary matching to reduce false positives
    words = set(w.strip(".,!?;:«»\"'()[]{}").lower() for w in text.split())
    for quest_name, quest in QUESTS_DATA.items():
        triggers = [t.lower() for t in quest.get("trigger_words", [])]
        if any((t in words) or (t in text) for t in triggers):
            if quest_name == "испытание завесы":
                await send_veil_invitation(update, quest_name)
            else:
                await start_quest(update, context, quest_name)
            break

async def send_veil_invitation(update: Update, quest_name: str):
    keyboard = [
        [InlineKeyboardButton("🔮 Войти в Завесу", callback_data=f"enter_{quest_name}")],
        [InlineKeyboardButton("⚖️ Отступить", callback_data=f"decline_{quest_name}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌒 Завеса шевелится...\n🕯 Нить реальности истончается...\nТы можешь:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()
    data = query.data
    # Robust split: ensure we have a delimiter
    parts = data.split("_", 1)
    if len(parts) != 2:
        return
    action, quest_name = parts[0], parts[1]
    quest = QUESTS_DATA.get(quest_name, {})

    if action == "enter":
        await query.edit_message_text(quest.get("on_accept", "Ты вошёл в квест..."))
        await start_quest(update, context, quest_name)
    elif action == "decline":
        await query.edit_message_text(f"⚖️ {quest.get('confirmation_text', 'Отменено.')}")

async def start_quest(update: Update, context: ContextTypes.DEFAULT_TYPE, quest_name: str):
    chat_id, incoming_thread = message_chat_and_thread(update)
    if not chat_id:
        return

    quest = QUESTS_DATA.get(quest_name, {})
    thread_id = incoming_thread

    # Create forum topic if possible and not already in a thread
    if thread_id is None and quest.get("room_name"):
        try:
            thread = await context.bot.create_forum_topic(chat_id=chat_id, name=quest.get("room_name", quest_name))
            thread_id = thread.message_thread_id
        except Exception as e:
            # Forums might be unavailable; proceed without thread
            print(f"ℹ️ Не удалось создать топик: {e}")

    # Send media groups in chunks of 10
    arts = get_arts(quest_name)
    for i in range(0, len(arts), 10):
        group = []
        files = []
        try:
            for a in arts[i:i+10]:
                f = open(a, "rb")
                files.append(f)  # keep refs to avoid GC before send
                group.append(InputMediaPhoto(media=InputFile(f, filename=os.path.basename(a))))
            if group:
                await context.bot.send_media_group(chat_id=chat_id, media=group, message_thread_id=thread_id)
        except Exception as e:
            print(f"⚠️ Ошибка при отправке медиа-группы: {e}")
        finally:
            for f in files:
                try:
                    f.close()
                except:
                    pass

    # Intro text
    intro_text = quest.get("intro_text", "Квест начинается...")
    await context.bot.send_message(chat_id=chat_id, text=intro_text, message_thread_id=thread_id)

def main():
    print("⚡ Бот запускается...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, quest_trigger))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Бот запущен! Ждём сообщений...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
