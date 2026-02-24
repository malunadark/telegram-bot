from aiogram import Router, types
from aiogram.filters import Command
from database import get_user, create_user

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    user = await get_user(message.from_user.id)

    if not user:
        await create_user(message.from_user.id, message.from_user.username)

        await message.answer(
            "Инициализация протокола N-0...\n"
            "Сканирование поведенческой модели...\n\n"
            "Ответьте честно.\n"
            "Вы бы рискнули собой ради незнакомца?"
        )
    else:
        await message.answer("Протокол уже активен.")
