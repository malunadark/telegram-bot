from aiogram import Router, types
from database import update_stat

router = Router()

@router.message(lambda m: m.text in ["Да", "Нет"])
async def first_choice(message: types.Message):
    if message.text == "Да":
        await update_stat(message.from_user.id, "sacrifice", 2)
        await update_stat(message.from_user.id, "risk", 1)

        await message.answer("Записано.\nОтклонение от среднего: +12%.\n\nВы слышите сигнал в тумане.")

    else:
        await update_stat(message.from_user.id, "rationality", 2)
        await update_stat(message.from_user.id, "stress", 1)

        await message.answer("Записано.\nСтабильность подтверждена.\n\nГруппа смотрит на вас.")
