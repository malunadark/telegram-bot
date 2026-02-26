import random
from aiogram.types import Message
from aiogram.filters import Command


def register_media(dp):

    music_links = [
        "https://youtu.be/1ZYbU82GVz4",
        "https://youtu.be/DuI0PzS3t9g"
    ]

    images = [
        "https://picsum.photos/800/600?grayscale",
        "https://picsum.photos/800/600?blur"
    ]

    @dp.message(Command("music"))
    async def send_music(message: Message):
        link = random.choice(music_links)
        await message.answer(f"🌫 Туман приносит звук:\n{link}")

    @dp.message(Command("image"))
    async def send_image(message: Message):
        img = random.choice(images)
        await message.answer_photo(img, caption="Из глубины.")
