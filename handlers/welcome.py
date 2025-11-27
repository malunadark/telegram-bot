from telegram import Update
from telegram.ext import ChatMemberHandler, ContextTypes
from config import GROUP_ID

async def greet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member and update.my_chat_member.new_chat_member.status == "member":
        await context.bot.send_message(
            chat_id=GROUP_ID,
            text="✨ Добро пожаловать в NOSTAI!"
        )

welcome_handler = ChatMemberHandler(greet, ChatMemberHandler.MY_CHAT_MEMBER)
