import sqlite3
from app.utils.helpers import get_database_path

def get_connection():
    db_path = get_database_path()
    return sqlite3.connect(db_path)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        password TEXT,
        language TEXT,
        character INTEGER,
        duration INTEGER,
        background INTEGER
    )
    """)
    cursor.execute("INSERT OR IGNORE INTO settings (id, password, language, character, duration, background) VALUES (1, 'admin', 'English', 1, 10, 2)")
    conn.commit()
    conn.close()

def get_saved_setting(key):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {key} FROM settings WHERE id = 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def update_setting(key, value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE settings SET {key} = ? WHERE id = 1", (value,))
    conn.commit()
    conn.close()