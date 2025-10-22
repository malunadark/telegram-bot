import random
from telegram import Update
from telegram.ext import ContextTypes

RUNES = [
    "ᚠ Fehu — богатство и изобилие.",
    "ᚢ Uruz — сила и выносливость.",
    "ᚦ Thurisaz — испытания и защита.",
    "ᚨ Ansuz — вдохновение и мудрость.",
    "ᚱ Raido — путь и путешествие.",
    "ᚲ Kenaz — огонь и знания.",
    "ᚷ Gebo — подарок и дружба.",
    "ᚸ Wunjo — радость и счастье.",
    "ᛁ Hagalaz — разрушение и перемены.",
    "ᛇ Eihwaz — преодоление препятствий.",
    "ᛉ Algiz — защита и охрана.",
    "ᛈ Sowilo — солнце и просветление.",
    "ᛋ Teiwaz — победа и храбрость.",
    "ᛏ Berkano — жизнь и возрождение.",
    "ᛐ Ehwaz — союз и сотрудничество.",
    "ᛒ Mannaz — человечество и общество.",
    "ᛖ Laguz — вода и интуиция.",
    "ᛗ Ingwaz — плодородие и завершение.",
    "ᛚ Othala — наследие и дом.",
    "ᛏ Dagaz — рассвет и изменение."
]

async def runa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected_rune = random.choice(RUNES)
    await update.message.reply_text(f"Ваша руна: {selected_rune}")
