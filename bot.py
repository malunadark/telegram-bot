import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import connect
from handlers import start, episode1

async def main():
    await connect()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(episode1.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
