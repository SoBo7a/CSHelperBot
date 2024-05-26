import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../../../data/play.db')

def init_db_play():
    """
    Initialize the play database.

    This function creates the 'subscriptions' table in the play database if it doesn't already exist.

    Args:
        None

    Returns:
        None
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL
            )
        ''')
        conn.commit()

def add_subscription(user_id: str, username: str):
    """
    Add a subscription to the play database.

    This function inserts a new subscription (user ID and username) into the 'subscriptions' table of the play database.

    Args:
        user_id (str): The ID of the user to add to the subscriptions.
        username (str): The username of the user to add to the subscriptions.

    Returns:
        None
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO subscriptions (user_id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()

def get_subscriptions():
    """
    Retrieve all subscriptions from the play database.

    This function retrieves all subscriptions (user ID and username) from the 'subscriptions' table of the play database.

    Args:
        None

    Returns:
        list: A list of tuples containing user IDs and usernames.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, username FROM subscriptions')
        return [(row[0], row[1]) for row in cursor.fetchall()]

def delete_subscriptions(user_id: str):
    """
    Delete a subscription from the play database.

    This function deletes a subscription (user ID and username) from the 'subscriptions' table of the play database.

    Args:
        user_id (str): The ID of the user whose subscription is to be deleted.

    Returns:
        None
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscriptions WHERE user_id = ?", (user_id,))
        conn.commit()
