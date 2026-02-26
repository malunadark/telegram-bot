import random
from aiogram.types import Message
from aiogram.filters import Command


def register_control(dp):

    # -------------------------
    # АКТИВАЦИЯ КВЕСТА
    # -------------------------

    @dp.message(Command("questline"))
    async def activate_quest(message: Message):
        await message.answer(
            "🌫 Квестовая линия активирована.\n\n"
            "Чтобы войти в глубину — используй /enter"
        )

    # -------------------------
    # СЛУЧАЙНОЕ ИЗОБРАЖЕНИЕ
    # -------------------------

    images = [
        "https://picsum.photos/800/600?grayscale",
        "https://picsum.photos/800/600?blur",
        "https://picsum.photos/800/600?random=1"
    ]

    @dp.message(Command("image"))
    async def send_image(message: Message):
        img = random.choice(images)
        await message.answer_photo(
            img,
            caption="🌫 Туман показывает обрывок реальности."
        )

    # -------------------------
    # МУЗЫКА
    # -------------------------

    music_links = [
        "https://youtu.be/1ZYbU82GVz4",
        "https://youtu.be/DuI0PzS3t9g",
        "https://youtu.be/4WtL5Qqz3lE"
    ]

    @dp.message(Command("music"))
    async def send_music(message: Message):
        link = random.choice(music_links)
        await message.answer(
            f"🎵 Туман приносит звук издалека:\n{link}"
        )

    # -------------------------
    # РУНА / АТМОСФЕРНОЕ СОБЫТИЕ
    # -------------------------

    runes = [
        "ᚠ — Потеря перед обретением.",
        "ᚢ — То, что ты ищешь, ищет тебя.",
        "ᚦ — Страх — это дверь.",
        "ᚨ — Ты уже глубже, чем думаешь."
    ]

    @dp.message(Command("rune"))
    async def send_rune(message: Message):
        rune = random.choice(runes)
        await message.answer(f"🔮 {rune}")

    # -------------------------
    # МИРОВОЕ СОБЫТИЕ
    # -------------------------

    events = [
        "🌑 В мире стало тише. Кто-то сделал выбор.",
        "🌫 Туман сегодня плотнее обычного.",
        "👁 Кажется, за беседой наблюдают.",
        "⚖ Сегодня карма имеет вес."
    ]

    @dp.message(Command("event"))
    async def world_event(message: Message):
        event = random.choice(events)
        await message.answer(event)
