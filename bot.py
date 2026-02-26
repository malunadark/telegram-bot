import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


def get_greeting(full_name: str) -> str:
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return (
            f"🌅 <b>{full_name}</b> вошёл в рассвет Nostai.\n\n"
            "Туман ещё держится у земли.\n"
            "Свет осторожен.\n"
            "День только делает первый вдох.\n\n"
            "Будь внимателен."
        )

    elif 12 <= hour < 17:
        return (
            f"☀ <b>{full_name}</b> ступил под дневное небо Nostai.\n\n"
            "Иллюзии становятся чётче.\n"
            "Слова звучат громче.\n"
            "Но правда всё ещё прячется.\n\n"
            "Выбор — только за тобой."
        )

    elif 17 <= hour < 22:
        return (
            f"🌆 <b>{full_name}</b> вошёл в закат Nostai.\n\n"
            "Тени удлиняются.\n"
            "Шёпот становится ближе.\n"
            "Грань между явью и дымом тонка.\n\n"
            "Смотри глубже."
        )

    elif 22 <= hour < 24:
        return (
            f"🌙 <b>{full_name}</b> вступил в ночь Nostai.\n\n"
            "Дым гуще, чем кажется.\n"
            "Шаги звучат иначе.\n"
            "Не всё, что видишь — существует.\n\n"
            "Не теряй себя."
        )

    else:  # 00:00–04:59
        return (
            f"🌑 <b>{full_name}</b> появился в глубокой ночи Nostai.\n\n"
            "Мир почти спит.\n"
            "Но не всё вокруг безмолвно.\n"
            "Некоторые двери открываются только сейчас.\n\n"
            "Ты уверен, что готов?"
        )


@dp.message(CommandStart())
async def start_handler(message: Message):
    text = get_greeting(message.from_user.full_name)
    await message.answer(text)


async def main():
    await dp.start_polling(bot)
    
from quest_engine import register_quest_handlers
register_quest_handlers(dp)

from control_panel import register_control
register_control(dp)

if __name__ == "__main__":
    asyncio.run(main())


