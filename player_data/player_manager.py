import json
import os

FILE = "player_data/players.json"

def load_players():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_players(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def set_stage(user_id, quest_id, stage):
    data = load_players()
    data[str(user_id)] = {
        "quest": quest_id,
        "stage": stage
    }
    save_players(data)

def get_player(user_id):
    data = load_players()
    return data.get(str(user_id))
