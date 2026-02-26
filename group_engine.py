from aiogram import F
from aiogram.types import Message
from database import update_stat, get_stat


def register_group(dp):

    @dp.message()
    async def monitor_group(message: Message):
        if message.chat.type == "private":
            return

        if not message.text:
            return

        text = message.text.lower()

        toxic_words = ["дурак", "идиот", "тупой"]

        for word in toxic_words:
            if word in text:
                karma = get_stat(message.from_user.id, "karma")
                update_stat(message.from_user.id, "karma", karma - 2)

                await message.reply(
                    "🌫 Туман реагирует на напряжение.\n"
                    "Некоторые двери могут закрыться."
                )
                break
