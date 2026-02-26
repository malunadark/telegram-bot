QUEST = {
    "id": "quest_001",
    "title": "Шепот Тумана",

    "stages": {

        "start": {
            "text": "Ты входишь в туман.",
            "media": {
                "image": "assets/images/quests/forest.jpg",
                "music": "assets/music/ambient/mist.mp3"
            },
            "choices": {
                "Идти глубже": "deep",
                "Остановиться": "stop"
            }
        },

        "deep": {
            "text": "Ты слышишь шёпот.",
            "media": {
                "gif": "assets/gifs/visions/shadow.gif"
            },
            "choices": {
                "Ответить": "answer",
                "Игнорировать": "ignore"
            }
        },

        "answer": {
            "text": "Шёпот принимает тебя.",
            "end": True
        },

        "ignore": {
            "text": "Туман сжимается.",
            "end": True
        },

        "stop": {
            "text": "Ты уходишь. Но туман запоминает.",
            "end": True
        }
    }
}
