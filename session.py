import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'medical_program.db'
SESSION_DURATION = timedelta(hours=24)

def create_session(user_id: int):
    created_at = datetime.now()
    expires_at = created_at + SESSION_DURATION

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Очистити стару сесію для цього користувача (опціонально)
        cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))

        # Генерація унікального токена для сесії (можна використовувати різні методи, залежно від вашого проекту)
        session_token = generate_session_token()

        cursor.execute('''
            INSERT INTO sessions (user_id, session_token, created_at, expires_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, session_token, created_at.isoformat(), expires_at.isoformat()))
        conn.commit()

def generate_session_token():
    return str(datetime.now().timestamp())

def get_session_user_id():
    now = datetime.now().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_id FROM sessions
            WHERE expires_at > ?
            ORDER BY created_at DESC
            LIMIT 1
        ''', (now,))
        row = cursor.fetchone()
        return row[0] if row else None

def is_session_active():
    return get_session_user_id() is not None

def clear_session(user_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
        conn.commit()

def refresh_session(user_id: int):
    clear_session(user_id)
    create_session(user_id)
