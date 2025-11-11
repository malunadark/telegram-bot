import os
from flask import Flask, request
from telegram import Bot, Update
from bot import create_app
from config import TOKEN

flask_app = Flask(__name__)
bot = Bot(TOKEN)
app_telegram = create_app()

WEBHOOK_PATH = '/api/webhook'
WEBHOOK_URL = f'https://<your-vercel-domain>{WEBHOOK_PATH}'

@flask_app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    app_telegram.update_queue.put(update)
    return 'OK'

@flask_app.route('/', methods=['GET'])
def home():
    return '🔥 Nostai Telegram Bot is alive.'

if __name__ == '__main__':
    bot.set_webhook(WEBHOOK_URL)
    flask_app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))