import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../../data/play.db')

def init_db_play():
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
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO subscriptions (user_id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()

def get_subscriptions():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, username FROM subscriptions')
        return [(row[0], row[1]) for row in cursor.fetchall()]

def delete_subscriptions(user_id: str):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscriptions WHERE user_id = ?", (user_id,))
        conn.commit()
