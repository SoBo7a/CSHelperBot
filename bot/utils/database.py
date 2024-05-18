import sqlite3
import os


def get_db_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, '../../data/stats.db')
    return db_path


def init_db():
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            discord_id TEXT PRIMARY KEY,
            discord_username TEXT NOT NULL,
            steam_id TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def add_user(discord_id: str, discord_username: str, steam_id: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO users (discord_id, discord_username, steam_id)
        VALUES (?, ?, ?)
    ''', (discord_id, discord_username, steam_id))
    conn.commit()
    conn.close()


def get_steam_id(discord_id: str) -> str:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT steam_id FROM users WHERE discord_id = ?
    ''', (discord_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None