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
        depth INTEGER DEFAULT 0,
        alignment_light INTEGER DEFAULT 0,
        alignment_dark INTEGER DEFAULT 0,
        alignment_reject INTEGER DEFAULT 0,
        faction TEXT DEFAULT NULL
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

    # =========================
    # ПРОЛОГ
    # =========================

    @dp.message(Command("prologue"))
    async def start_prologue(message: Message):
        get_player(message.from_user.id, message.from_user.full_name)

        update(message.from_user.id, "stage", "prologue_1")

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Ответить светом", callback_data="p_signal")],
                [InlineKeyboardButton(text="Скрыться", callback_data="p_hide")],
                [InlineKeyboardButton(text="Уйти глубже", callback_data="p_deeper")]
            ]
        )

        await message.answer(
            "Ты приходишь в себя среди холодного леса.\n\n"
            "Вдалеке вспыхивает луч.\n"
            "Он ищет выживших.\n"
            "Или отмечает цели.\n\n"
            "Ты действуешь.",
            reply_markup=keyboard
        )

    # ------------------------
    # ПРОЛОГ ЛОГИКА
    # ------------------------

    @dp.callback_query(F.data.startswith("p_"))
    async def prologue_flow(callback: CallbackQuery):

        user_id = callback.from_user.id
        stage = get(user_id, "stage")

        # --- Первый выбор

        if callback.data == "p_signal":
            update(user_id, "alignment_light", get(user_id, "alignment_light") + 1)
            update(user_id, "fear", get(user_id, "fear") + 3)

        elif callback.data == "p_hide":
            update(user_id, "alignment_reject", get(user_id, "alignment_reject") + 1)

        elif callback.data == "p_deeper":
            update(user_id, "alignment_dark", get(user_id, "alignment_dark") + 1)
            update(user_id, "fear", get(user_id, "fear") + 5)

        # Проверка фракции

        light = get(user_id, "alignment_light")
        dark = get(user_id, "alignment_dark")
        reject = get(user_id, "alignment_reject")

        faction_text = None

        if light >= 3:
            update(user_id, "faction", "Пришедшие")
            faction_text = (
                "Свет больше не дрожит.\n\n"
                "Голос становится твёрдым:\n"
                "«Мы выведем тебя».\n\n"
                "Ты сделал выбор."
            )

        elif dark >= 3:
            update(user_id, "faction", "Падшие")
            faction_text = (
                "Лес перестаёт быть враждебным.\n\n"
                "Он принимает тебя.\n"
                "Ты слышишь больше, чем должен."
            )

        elif reject >= 3:
            update(user_id, "faction", "Отвергнутые")
            faction_text = (
                "Ни свет, ни глубина не принимают тебя полностью.\n\n"
                "Ты будешь идти один.\n"
                "И это твой путь."
            )

        # Если фракция выбрана — финал пролога

        if faction_text:
            update(user_id, "stage", "faction_locked")
            await callback.message.edit_text(faction_text)
            await callback.answer()
            return

        # Если нет — продолжаем

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Продолжить путь", callback_data="p_continue")]
            ]
        )

        await callback.message.edit_text(
            "Мир реагирует на твой выбор.\n\n"
            "Но решение ещё не окончательно.\n"
            "Ты идёшь дальше.",
            reply_markup=keyboard
        )

        await callback.answer()

    # =========================
    # СТАРЫЙ ENTER (ОСТАВЛЕН)
    # =========================

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

    # =========================
    # ПРОФИЛЬ
    # =========================

    @dp.message(Command("profile"))
    async def profile(message: Message):
        await message.answer(
            f"Фракция: {get(message.from_user.id, 'faction')}\n"
            f"Глубина: {get(message.from_user.id, 'depth')}\n"
            f"XP: {get(message.from_user.id, 'xp')}\n"
            f"Карма: {get(message.from_user.id, 'karma')}\n"
            f"Страх: {get(message.from_user.id, 'fear')}"
        )
