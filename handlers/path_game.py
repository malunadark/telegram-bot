from telegram import InputFile
import os

# Путь к папке с изображениями
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, 'images', 'horror')

# Словарь с картинками для квестов
IMAGES = {
    "tuman_ravnina": os.path.join(IMAGES_DIR, "1_tuman_ravnina.png"),
    "lager_volonterov": os.path.join(IMAGES_DIR, "2_lager_volonterov.png"),
    "raskopannyi_pepel": os.path.join(IMAGES_DIR, "3_raskopannyi_pepel.png"),
    "stancia_mchs": os.path.join(IMAGES_DIR, "4_stancia_mchs.png"),
}

# Пример использования
async def start_horror_quest(update, context):
    """
    Начало квеста: отправка изображения и текста.
    """
    chat_id = update.effective_chat.id
    await context.bot.send_photo(chat_id=chat_id, photo=InputFile(IMAGES["tuman_ravnina"]))
    await context.bot.send_message(chat_id=chat_id, text="Ты оказываешься на туманной равнине...")
