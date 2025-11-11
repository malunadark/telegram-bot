import os, json, logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from config import TOKEN, IMAGES_DIR, QUEST_FILE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GROUP_ID = -1001234567890  # <- твоя группа

# --- Загрузка квестов ---
with open(QUEST_FILE, "r", encoding="utf-8") as f:
    QUESTS = json.load(f)["quests"]

# --- Приветствие новых участников ---
async def greet_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:
        await update.message.reply_text(f"Привет, {user.first_name}! Добро пожаловать в квест.")

# --- Запуск квеста ---
async def start_quest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.replace("/", "").lower()
    quest = QUESTS.get(cmd)
    if not quest:
        await update.message.reply_text("❌ Неизвестный квест.")
        return

    forum_topics = await context.bot.getForumTopicList(chat_id=GROUP_ID)
    existing_topic = None
    for topic in forum_topics.forum_topics:
        if topic.name == quest.get("title", cmd):
            existing_topic = topic
            break

    if existing_topic:
        await update.message.reply_text(f"Квест '{quest.get('title', cmd)}' уже существует.")
        await context.bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=existing_topic.message_thread_id,
            text=f"🔮 {update.effective_user.first_name} возвращается в квест **{quest.get('title', cmd)}**..."
        )
    else:
        new_topic = await context.bot.createForumTopic(chat_id=GROUP_ID, name=quest.get("title", cmd))
        await context.bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=new_topic.message_thread_id,
            text=quest.get("text", "")
        )
        for img_name in quest.get("images", []):
            img_path = os.path.join(IMAGES_DIR, img_name)
            if os.path.exists(img_path):
                await context.bot.send_photo(chat_id=GROUP_ID,
                                             message_thread_id=new_topic.message_thread_id,
                                             photo=InputFile(img_path))
            else:
                await context.bot.send_message(chat_id=GROUP_ID,
                                               message_thread_id=new_topic.message_thread_id,
                                               text=f"⚠️ Не найдено изображение: {img_name}")
        await update.message.reply_text(f"✨ Создана новая тема: {quest.get('title', cmd)}")

# --- Создание приложения ---
def create_app():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_user))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start_quest))
    return app
