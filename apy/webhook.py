from telegram import Bot, Update
from bot import create_app
from config import TOKEN

bot = Bot(TOKEN)

async def handler(request):
    if request.method != "POST":
        return {"status": 200, "body": "ok"}

    update_json = await request.json()
    update = Update.de_json(update_json, bot)

    app_telegram = create_app()
    await app_telegram.process_update(update)

    return {"status": 200, "body": "ok"}
