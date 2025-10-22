from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler
from config import ASSETS_DIR

# Определение состояний
CHOOSING_PATH, ENCOUNTER, RESOLVE, FINAL = range(4)

# Имитация данных квеста (формат JSON)
QUESTS = {
    "start": {
        "text": "Ты стоишь на пороге двух дорог. Первая дорога ведёт в мрачный лес, вторая — в тихую долину. Куда пойдёшь?",
        "options": [
            ("🌳 Лес", "forest"),
            ("🌿 Долина", "valley")
        ],
        "image": "forest.gif"
    },
    "forest": {
        "text": "В лесу тебя встречает дух огня. Он хочет испытать твою смелость. Что сделаешь?",
        "options": [
            ("🔥 Принять испытание", "accept"),
            ("🔺 Уклониться", "decline")
        ],
        "image": "forest_fire.gif"
    },
    # Другие состояния квеста…
}

async def start_path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = QUESTS["start"]
    keyboard = [[InlineKeyboardButton(text, callback_data=cb)] for text, cb in question["options"]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(question["text"], reply_markup=reply_markup)
    return CHOOSING_PATH

async def choose_path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    next_state = query.data
    await process_step(next_state, update, context)
    return CHOOSING_PATH

async def process_step(state, update, context):
    step = QUESTS[state]
    text = step["text"]
    options = step.get("options", [])
    if options:
        keyboard = [[InlineKeyboardButton(text, callback_data=cb)] for text, cb in options]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(text)

# Остальные обработчики квеста...

def register(app):
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_path)],
        states={CHOOSING_PATH: [CallbackQueryHandler(choose_path)]},
        fallbacks=[],
        map_to_parent={"FINISH": ConversationHandler.END}
    )
    app.add_handler(conv_handler)