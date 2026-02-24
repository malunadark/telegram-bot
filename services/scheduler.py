import asyncio
from aiogram import Bot

async def delayed_message(bot: Bot, telegram_id: int, text: str, delay: int):
    await asyncio.sleep(delay)
    await bot.send_message(telegram_id, text)
  from services.scheduler import delayed_message
import asyncio

asyncio.create_task(
    delayed_message(
        message.bot,
        message.from_user.id,
        "Мы пересчитали вашу модель. Вероятность критического выбора растет.",
        120  # 2 минуты
    )
)
