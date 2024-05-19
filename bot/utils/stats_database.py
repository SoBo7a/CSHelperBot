import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../../data/stats.db')


def init_db_stats():
    """
    Initialize the database for storing user statistics.
    Creates the 'users' table if it doesn't exist.
    """
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                discord_id TEXT PRIMARY KEY,
                discord_username TEXT NOT NULL,
                steam_id TEXT NOT NULL
            )
        ''')
        conn.commit()


def add_user(discord_id: str, discord_username: str, steam_id: str):
    """
    Add or update a user's information in the database.

    Args:
        discord_id (str): The Discord ID of the user.
        discord_username (str): The Discord username of the user.
        steam_id (str): The Steam ID of the user.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO users (discord_id, discord_username, steam_id)
            VALUES (?, ?, ?)
        ''', (discord_id, discord_username, steam_id))
        conn.commit()


def get_steam_id(discord_id: str) -> str:
    """
    Retrieve the Steam ID associated with a Discord ID from the database.

    Args:
        discord_id (str): The Discord ID of the user.

    Returns:
        str: The Steam ID associated with the Discord ID, or None if not found.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT steam_id FROM users WHERE discord_id = ?
        ''', (discord_id,))
        result = c.fetchone()
        
    if result:
        return result[0]
    else:
        return None
