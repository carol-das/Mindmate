import sqlite3
import os
from datetime import datetime

# Local database file path (Sensitive Cubicle Model)
DB_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "data", "mindmate_vault.db")

def init_db():
    """Initializes the local SQLite database for mood logging and memory control."""
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS mood_logs ( id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, mood_score INTEGER NOT NULL, note TEXT ) ''')
    conn.commit()
    conn.close()

def log_mood(mood_score: int, note: str = ""):
    """Logs a mood entry locally with a timestamp."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO mood_logs (timestamp, mood_score, note) VALUES (?, ?, ?) ''', (datetime.now().strftime("%Y-%m-%d %H:%M"), mood_score, note))
    conn.commit()
    conn.close()

def get_mood_history():
    """Fetches all local mood entries."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, mood_score, note FROM mood_logs ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def purge_vault():
    """Completely clears all local database entries, enforcing user data sovereignty."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM mood_logs')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    log_mood(4, "Feeling hopeful before starting therapy preparation.")
    print("--- Local Vault Initialized ---")
    print("Test Mood Logged Successfully.")
    print("Current History:", get_mood_history())