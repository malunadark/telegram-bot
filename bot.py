import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram import Router
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()
dp.include_router(router)


# 🌫 Приветствие новых участников
@router.message(F.new_chat_members)
async def welcome_new_member(message: Message):
    for member in message.new_chat_members:
        
        # Удаляем системное сообщение "X joined the group"
        try:
            await message.delete()
        except:
            pass

        await asyncio.sleep(1.5)

        await message.answer(
            f"🌫 <b>{member.full_name}</b> Вошёл в туман Nostai.\n\n"
            "Дым здесь гуще, чем кажется.\n"
            "Слова — не всегда правда.\n"
            "Выбор — только за тобой.\n\n"
            "Будь внимателен."
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
