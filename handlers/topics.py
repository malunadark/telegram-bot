from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
from config import GROUP_ID

async def create_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != GROUP_ID:
        return
    
    if update.message.text.startswith("!тема"):
        title = update.message.text.replace("!тема", "").strip()
        topic = await update.effective_chat.create_forum_topic(title)
        await update.message.reply_text(f"✔ Тема создана: {title}")

topic_handler = MessageHandler(filters.TEXT & filters.Regex(r"^!тема"), create_topic)
