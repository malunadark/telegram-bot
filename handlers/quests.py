import json
from telegram import Update, InputFile
from telegram.ext import MessageHandler, filters, ContextTypes

from config import QUEST_FILE, IMAGES_DIR, GROUP_ID

with open(QUEST_FILE, 'r', encoding='utf-8') as f:
    QUESTS = json.load(f)["quests"]

async def run_quest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != GROUP_ID:
        return

    cmd = update.message.text.replace("/", "").lower()
    quest = QUESTS.get(cmd)

    if not quest:
        return

    # Отправляем текст
    await update.message.reply_text(quest["text"])

    # Отправляем изображения
    for img in quest.get("images", []):
        path = f"{IMAGES_DIR}/{img}"
        await update.message.reply_photo(InputFile(path))

quest_handler = MessageHandler(filters.TEXT & filters.Regex(r"^/"), run_quest)
