# game_data/quests/prologue.py

import random


# =========================
# СОЗДАНИЕ ИГРОКА
# =========================

def create_player():
    return {
        "quest": "prologue",
        "stage": "intro",
        "hp": 100,
        "fear": 0,
        "karma": 0,
        "alignment_light": 0,
        "alignment_dark": 0,
        "alignment_reject": 0,
        "faction_locked": False,
        "faction": None
    }


# =========================
# ВСТУПИТЕЛЬНАЯ СЦЕНА
# =========================

def intro_scene(player):

    text = (
        "Ты не помнишь, как оказался здесь.\n\n"
        "Лес вокруг не шумит.\n"
        "Он не живёт.\n"
        "Он наблюдает.\n\n"
        "Где-то вдалеке мигает направленный луч света.\n"
        "Кто-то ищет.\n"
        "Или проверяет, кто ещё остался."
    )

    choices = {
        "Подать сигнал в ответ": "signal",
        "Скрыться и наблюдать": "hide",
        "Уйти глубже в лес": "deeper"
    }

    return text, choices


# =========================
# ПРИМЕНЕНИЕ ВЫБОРА
# =========================

def apply_alignment(player, choice):

    if choice == "signal":
        player["alignment_light"] += 1
        player["fear"] += 5

    elif choice == "hide":
        player["alignment_reject"] += 1
        player["fear"] += 2

    elif choice == "deeper":
        player["alignment_dark"] += 1
        player["fear"] += 7

    return player


# =========================
# ВТОРАЯ СЦЕНА
# =========================

def second_scene(player):

    base_text = (
        "Воздух становится плотнее.\n\n"
        "Ты ощущаешь, что за тобой наблюдают.\n"
        "Не глазами.\n"
        "Чем-то другим."
    )

    if player["fear"] > 20:
        base_text += "\n\nТвоё дыхание сбивается. Паника начинает управлять телом."

    if player["alignment_dark"] > 0:
        base_text += "\n\nГлубина будто принимает тебя."

    if player["alignment_light"] > 0:
        base_text += "\n\nГде-то впереди слышен голос. Чёткий. Военный."

    choices = {
        "Продолжать идти": "forward",
        "Окликнуть тех, кто впереди": "call",
        "Спрятаться": "cover"
    }

    return base_text, choices


# =========================
# РАЗРЕШЕНИЕ ВТОРОГО ВЫБОРА
# =========================

def resolve_second_choice(player, choice):

    if choice == "forward":
        player["fear"] += 5

        text = (
            "Ты делаешь шаг.\n"
            "Под ногами что-то хрустит.\n"
            "Это не ветка.\n\n"
            f"Страх +5 (теперь {player['fear']})"
        )

    elif choice == "call":
        player["alignment_light"] += 1
        player["karma"] += 1

        text = (
            "— Эй! Есть кто?\n\n"
            "Свет останавливается.\n"
            "Теперь он направлен прямо на тебя.\n\n"
            f"Склонность к Свету +1"
        )

    elif choice == "cover":
        player["alignment_reject"] += 1
        player["fear"] += 3

        text = (
            "Ты прячешься за поваленным стволом.\n"
            "Луч проходит в метре от тебя.\n\n"
            f"Страх +3 (теперь {player['fear']})"
        )

    else:
        text = "Ты замираешь."

    return text, player


# =========================
# ПРОВЕРКА ФРАКЦИИ
# =========================

def check_faction_lock(player):

    if player["faction_locked"]:
        return player

    if player["alignment_light"] >= 3:
        player["faction"] = "Пришедшие"
        player["faction_locked"] = True

    elif player["alignment_dark"] >= 3:
        player["faction"] = "Падшие"
        player["faction_locked"] = True

    elif player["alignment_reject"] >= 3:
        player["faction"] = "Отвергнутые"
        player["faction_locked"] = True

    return player


# =========================
# ЭФФЕКТЫ СТРАХА
# =========================

def apply_fear_effects(player):

    if player["fear"] > 60:
        player["hp"] -= 5

    if player["hp"] <= 0:
        player["hp"] = 1
        player["alignment_reject"] += 1

    return player


# =========================
# ФИНАЛ ПРОЛОГА (ЕСЛИ ФРАКЦИЯ ОПРЕДЕЛЕНА)
# =========================

def faction_reveal(player):

    if not player["faction_locked"]:
        return None

    if player["faction"] == "Пришедшие":
        text = (
            "Луч света больше не дрожит.\n\n"
            "— Не двигаться.\n"
            "Мы выведем тебя отсюда.\n\n"
            "Твоя история только начинается."
        )

    elif player["faction"] == "Падшие":
        text = (
            "Лес перестаёт казаться враждебным.\n\n"
            "Глубина отвечает.\n\n"
            "Ты сделал правильный выбор.\n"
            "Теперь пути назад нет."
        )

    else:
        text = (
            "Ни свет, ни тьма не принимают тебя полностью.\n\n"
            "Ты сам выберешь, кем стать.\n"
            "И за это придётся платить."
        )

    return text
