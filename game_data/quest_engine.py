import asyncio
import sqlite3
from aiogram import F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.filters import Command

DB = "nostai_quest.db"


# ------------------------
# БАЗА ДАННЫХ
# ------------------------

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        stage TEXT DEFAULT 'none',
        xp INTEGER DEFAULT 0,
        karma INTEGER DEFAULT 0,
        fear INTEGER DEFAULT 0,
        depth INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def get_player(user_id, name):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM players WHERE user_id = ?", (str(user_id),))
    player = cur.fetchone()

    if not player:
        cur.execute("""
        INSERT INTO players (user_id, name)
        VALUES (?, ?)
        """, (str(user_id), name))
        conn.commit()

    conn.close()


def update(user_id, field, value):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(f"UPDATE players SET {field} = ? WHERE user_id = ?", (value, str(user_id)))
    conn.commit()
    conn.close()


def get(user_id, field):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(f"SELECT {field} FROM players WHERE user_id = ?", (str(user_id),))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else 0


# ------------------------
# РЕГИСТРАЦИЯ
# ------------------------

def register_quest_handlers(dp):

    init_db()

    # ------------------------
    # ВХОД В ИГРУ
    # ------------------------

    @dp.message(Command("enter"))
    async def enter_game(message: Message):
        get_player(message.from_user.id, message.from_user.full_name)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Войти", callback_data="q_begin")],
                [InlineKeyboardButton(text="Отступить", callback_data="q_leave")]
            ]
        )

        await message.answer(
            "Ты чувствуешь, что за этой дверью что-то есть.\n\n"
            "Возврата не будет.\n\n"
            "Ты входишь?",
            reply_markup=keyboard
        )

    # ------------------------
    # КВЕСТОВАЯ ЛОГИКА
    # ------------------------

    @dp.callback_query(F.data.startswith("q_"))
    async def quest_flow(callback: CallbackQuery):

        user_id = callback.from_user.id

        if callback.data == "q_begin":
            update(user_id, "stage", "forest")
            update(user_id, "depth", 1)
            update(user_id, "xp", get(user_id, "xp") + 5)

            await asyncio.sleep(2)

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Идти на шёпот", callback_data="q_whisper")],
                    [InlineKeyboardButton(text="Остаться в тишине", callback_data="q_stay")]
                ]
            )

            await callback.message.edit_text(
                "Ты входишь в туман.\n\n"
                "Шёпот зовёт тебя по имени.\n"
                "Но ты не помнишь, чтобы называл его кому-то.",
                reply_markup=keyboard
            )

        # --- ВЕТКА 1

        elif callback.data == "q_whisper":
            update(user_id, "fear", get(user_id, "fear") + 2)
            update(user_id, "karma", get(user_id, "karma") - 1)
            update(user_id, "depth", get(user_id, "depth") + 1)

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Коснуться тени", callback_data="q_touch")],
                    [InlineKeyboardButton(text="Спросить: кто ты?", callback_data="q_ask")]
                ]
            )

            await callback.message.edit_text(
                "Тень отделяется от земли.\n\n"
                "Она повторяет твои движения.\n"
                "Но с задержкой.",
                reply_markup=keyboard
            )

        # --- ВЕТКА 2

        elif callback.data == "q_stay":
            update(user_id, "karma", get(user_id, "karma") + 1)
            update(user_id, "depth", get(user_id, "depth") + 1)

            await callback.message.edit_text(
                "Ты остаёшься.\n\n"
                "И понимаешь — шёпот не вокруг.\n"
                "Он внутри тебя.\n\n"
                "Иногда тишина страшнее."
            )

        # --- ГЛУБОКАЯ ВЕТКА

        elif callback.data == "q_touch":
            update(user_id, "stage", "dark_path")
            update(user_id, "xp", get(user_id, "xp") + 20)
            update(user_id, "fear", get(user_id, "fear") + 5)

            await callback.message.edit_text(
                "Ты касаешься тени.\n\n"
                "Мир трескается.\n"
                "Воздух становится плотным.\n\n"
                "«Теперь ты видишь больше».\n\n"
                "🌑 Концовка: Принятие Тьмы."
            )

        elif callback.data == "q_ask":
            update(user_id, "stage", "awaken")
            update(user_id, "xp", get(user_id, "xp") + 15)

            await callback.message.edit_text(
                "Ты спрашиваешь.\n\n"
                "Ответ приходит не словами.\n\n"
                "Ты начинаешь вспоминать то,\n"
                "чего никогда не переживал.\n\n"
                "🌫 Концовка: Пробуждение."
            )

        elif callback.data == "q_leave":
            await callback.message.edit_text(
                "Ты делаешь шаг назад.\n\n"
                "Дверь остаётся приоткрытой.\n"
                "Она будет ждать."
            )

        await callback.answer()

    # ------------------------
    # ПРОФИЛЬ
    # ------------------------

    @dp.message(Command("profile"))
    async def profile(message: Message):
        await message.answer(
            f"Глубина: {get(message.from_user.id, 'depth')}\n"
            f"XP: {get(message.from_user.id, 'xp')}\n"
            f"Карма: {get(message.from_user.id, 'karma')}\n"
            f"Страх: {get(message.from_user.id, 'fear')}"
        )
