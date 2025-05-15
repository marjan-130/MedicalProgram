import sqlite3
import uuid
import os

DB_PATH = 'medical_program.db'
SESSION_FILE = 'session.txt'

def create_session(user_id):
    session_token = str(uuid.uuid4())
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (user_id, session_token) VALUES (?, ?)",
            (user_id, session_token)
        )
        conn.commit()

    with open(SESSION_FILE, "w") as f:
        f.write(session_token)

    return session_token

def is_session_active():
    if not os.path.exists(SESSION_FILE):
        return False
    with open(SESSION_FILE, "r") as f:
        token = f.read().strip()
    return bool(token)

def get_session_token():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        return f.read().strip()

def get_session_user_id():
    token = get_session_token()
    if not token:
        return None
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM sessions WHERE session_token = ?", (token,))
        result = cursor.fetchone()
        return result[0] if result else None

def clear_session():
    # Видалити session.txt
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

