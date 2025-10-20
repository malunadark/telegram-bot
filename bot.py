import os
import random
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]
ASSETS_DIR = "assets"

WELCOME_TEXT = """
𝕹𝖔𝖘𝖙𝖆𝖎 ✦ 𝕻𝖔𝖗𝖔𝖌 𝕿𝖆𝖎𝖓𝖞  

Добро пожаловать Придший...  
Войдя сюда, откинув сомнения, узрев туман...  
Стань бойцом, стань медиком, стань спасателем... 
Кем угодно стань...

✦ Избери путь...  
✦ войди в тайны мира  
✦ Стань частью круга Nostai.
"""

# Приветствие новых участников
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"🌑 Добро пожаловать, {member.mention_html()}!\n\n{WELCOME_TEXT}",
            parse_mode="HTML"
        )

# /start для личного чата
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот Nostai. 🌒\nНапиши /runa, /symbol или /mist, чтобы увидеть магию!"
    )

# Остальные команды
async def runa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    runes_dir = os.path.join(ASSETS_DIR, "runes")
    if not os.path.exists(runes_dir) or not os.listdir(runes_dir):
        await update.message.reply_text("❌ Папка runes пуста или не найдена.")
        return
    rune_file = random.choice(os.listdir(runes_dir))
    with open(os.path.join(runes_dir, rune_file), "rb") as photo:
        await update.message.reply_photo(photo, caption="✦ Руна пробуждена...")

async def symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbols_dir = os.path.join(ASSETS_DIR, "symbols")
    if not os.path.exists(symbols_dir) or not os.listdir(symbols_dir):
        await update.message.reply_text("❌ Папка symbols пуста или не найдена.")
        return
    symbol_file = random.choice(os.listdir(symbols_dir))
    with open(os.path.join(symbols_dir, symbol_file), "rb") as photo:
        await update.message.reply_photo(photo, caption="✦ Символ фракции проявился...")

async def mist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arts_dir = os.path.join(ASSETS_DIR, "arts")
    if not os.path.exists(arts_dir) or not os.listdir(arts_dir):
        await update.message.reply_text("❌ Папка arts пуста или не найдена.")
        return
    art_file = random.choice(os.listdir(arts_dir))
    with open(os.path.join(arts_dir, art_file), "rb") as photo:
        await update.message.reply_photo(photo, caption="✦ Туман скрывает истину...")

def main():
    app = Application.builder().token(TOKEN).build()

    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(CommandHandler("runa", runa))
    app.add_handler(CommandHandler("symbol", symbol))
    app.add_handler(CommandHandler("mist", mist))

    print("Бот запущен! Ждём команд и новых участников...")
    app.run_polling()

if __name__ == "__main__":
    main()
