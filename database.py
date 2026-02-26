import sqlite3

DB_NAME = "nostai.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        xp INTEGER DEFAULT 0,
        karma INTEGER DEFAULT 0,
        fear INTEGER DEFAULT 0,
        awareness INTEGER DEFAULT 0,
        stage TEXT DEFAULT 'none'
    )
    """)

    conn.commit()
    conn.close()


def get_player(user_id, name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players WHERE user_id = ?", (str(user_id),))
    player = cursor.fetchone()

    if not player:
        cursor.execute("""
            INSERT INTO players (user_id, name)
            VALUES (?, ?)
        """, (str(user_id), name))
        conn.commit()
        cursor.execute("SELECT * FROM players WHERE user_id = ?", (str(user_id),))
        player = cursor.fetchone()

    conn.close()
    return player


def update_stat(user_id, field, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE players SET {field} = ? WHERE user_id = ?", (value, str(user_id)))
    conn.commit()
    conn.close()


def get_stat(user_id, field):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT {field} FROM players WHERE user_id = ?", (str(user_id),))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
