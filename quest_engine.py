import asyncio
from aiogram import F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

from database import get_player, update_stat, get_stat


def register_quest(dp):

    @dp.message(Command("enter"))
    async def enter_game(message: Message):
        get_player(message.from_user.id, message.from_user.full_name)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Да", callback_data="q_start")],
                [InlineKeyboardButton(text="Нет", callback_data="q_exit")]
            ]
        )

        await message.answer(
            "Ты уверен, что хочешь войти?\n"
            "Возврата не будет.",
            reply_markup=keyboard
        )

    @dp.callback_query(F.data.startswith("q_"))
    async def quest_flow(callback: CallbackQuery):
        user_id = callback.from_user.id

        if callback.data == "q_start":
            update_stat(user_id, "stage", "forest")
            update_stat(user_id, "xp", get_stat(user_id, "xp") + 5)

            await asyncio.sleep(3)

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Идти на звук", callback_data="q_sound")],
                    [InlineKeyboardButton(text="Остаться", callback_data="q_wait")]
                ]
            )

            await callback.message.edit_text(
                "Ты входишь в туман.\n"
                "Слышится тихий шёпот.",
                reply_markup=keyboard
            )

        elif callback.data == "q_sound":
            update_stat(user_id, "fear", get_stat(user_id, "fear") + 2)
            update_stat(user_id, "karma", get_stat(user_id, "karma") - 1)

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Коснуться тени", callback_data="q_touch")],
                    [InlineKeyboardButton(text="Отступить", callback_data="q_back")]
                ]
            )

            await callback.message.edit_text(
                "Тень отделяется от земли.\n"
                "Она смотрит прямо в тебя.",
                reply_markup=keyboard
            )

        elif callback.data == "q_wait":
            update_stat(user_id, "awareness", get_stat(user_id, "awareness") + 2)
            await callback.message.edit_text(
                "Ты замечаешь, что шёпот не вокруг.\n"
                "Он внутри тебя."
            )

        elif callback.data == "q_touch":
            update_stat(user_id, "stage", "dark_path")
            update_stat(user_id, "xp", get_stat(user_id, "xp") + 20)

            await callback.message.edit_text(
                "Мир трескается.\n"
                "Ты слышишь голос:\n\n"
                "Теперь ты часть нас.\n\n"
                "🌑 Концовка Тени."
            )

        elif callback.data == "q_back":
            update_stat(user_id, "stage", "light_path")
            update_stat(user_id, "xp", get_stat(user_id, "xp") + 5)

            await callback.message.edit_text(
                "Ты отступаешь.\n"
                "Тень растворяется.\n"
                "Но она запомнила тебя."
            )

        elif callback.data == "q_exit":
            await callback.message.edit_text(
                "Ты делаешь шаг назад.\n"
                "Но туман остаётся."
            )

        await callback.answer()
