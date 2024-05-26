import sqlite3
import os
from datetime import datetime, timezone, timedelta

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../../../data/vac_check.db')


def init_db_vac():
    """
    Initializes the VAC database and creates the necessary table if it doesn't exist.

    Returns:
        None
    """
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS vac_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_user_id TEXT,
                steam_id TEXT,
                check_date TEXT,
                number_of_vac_bans INTEGER,
                days_since_last_ban INTEGER
            )
        ''')
        conn.commit()


def steam_id_exists(steam_id):
    """
    Checks if a Steam ID already exists in the database.

    Args:
        steam_id (str): The Steam ID to check.

    Returns:
        bool: True if the Steam ID exists, False otherwise.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM vac_checks WHERE steam_id = ?', (steam_id,))
        return c.fetchone() is not None
    

def insert_vac_check(discord_user_id, steam_id, number_of_vac_bans, days_since_last_ban):
    """
    Inserts a record into the database.

    Args:
        discord_user_id (str): The Discord user ID associated with the check.
        steam_id (str): The Steam ID to insert.
        number_of_vac_bans (int): The number of VAC bans associated with the Steam ID.
        days_since_last_ban (int): The number of days since the last VAC ban.

    Returns:
        None
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        check_date = datetime.now(timezone.utc)
        c.execute('''
            INSERT INTO vac_checks (discord_user_id, steam_id, check_date, number_of_vac_bans, days_since_last_ban)
            VALUES (?, ?, ?, ?, ?)
        ''', (discord_user_id, steam_id, check_date, number_of_vac_bans, days_since_last_ban))
        conn.commit()


def get_vac_checks():
    """
    Fetches all Steam IDs and ban information from the database.

    Returns:
        list: A list of tuples containing the fetched data.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT discord_user_id, steam_id, check_date, number_of_vac_bans, days_since_last_ban
            FROM vac_checks
        ''')
        return c.fetchall()
    

def delete_old_entries():
    """
    Deletes entries from the database that are older than 360 days.

    Returns:
        None
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        # Calculate the date 360 days ago
        old_date = datetime.now(timezone.utc) - timedelta(days=360)
        # Delete entries older than old_date
        c.execute('DELETE FROM vac_checks WHERE check_date <= ?', (old_date,))
        conn.commit()
    

def remove_entry_by_steam_id(steam_id):
    """
    Removes an entry from the database based on the given Steam ID.

    Args:
        steam_id (str): The Steam ID of the entry to be removed.

    Returns:
        None
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM vac_checks WHERE steam_id = ?', (steam_id,))
        conn.commit()