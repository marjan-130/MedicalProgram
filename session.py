import sqlite3
import uuid
from datetime import datetime, timedelta

DB_PATH = 'medical_program.db'


def create_session(user_id):
    session_token = str(uuid.uuid4())
    created_at = datetime.now()
    expires_at = created_at + timedelta(hours=24)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
            cursor.execute('''
                INSERT INTO sessions (user_id, session_token, created_at, expires_at)
                VALUES (?, ?, ?, ?)
            ''', (user_id, session_token, created_at.isoformat(), expires_at.isoformat()))
            conn.commit()
            print(f"✅ Сесію створено для користувача {user_id}")
    except sqlite3.Error as e:
        print(f"❌ Помилка створення сесії: {e}")


def is_session_active():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id, expires_at FROM sessions
                ORDER BY id DESC LIMIT 1
            ''')
            session = cursor.fetchone()

            if session:
                user_id, expires_at = session
                # Перевірка, чи expires_at є рядком
                if isinstance(expires_at, (bytes, bytearray)):
                    expires_at = expires_at.decode('utf-8')
                if isinstance(expires_at, str):
                    if datetime.now() < datetime.fromisoformat(expires_at):
                        return True
                    else:
                        cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
                        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Помилка перевірки сесії: {e}")
    return False


def get_session_user_id():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id, expires_at FROM sessions
                ORDER BY id DESC LIMIT 1
            ''')
            session = cursor.fetchone()

            if session:
                user_id, expires_at = session
                if isinstance(expires_at, (bytes, bytearray)):
                    expires_at = expires_at.decode('utf-8')
                if isinstance(expires_at, str):
                    if datetime.now() < datetime.fromisoformat(expires_at):
                        return user_id
    except sqlite3.Error as e:
        print(f"❌ Помилка отримання user_id з сесії: {e}")
    return None


def get_session_token():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT session_token, expires_at FROM sessions
                ORDER BY id DESC LIMIT 1
            ''')
            session = cursor.fetchone()

            if session:
                token, expires_at = session
                if isinstance(expires_at, (bytes, bytearray)):
                    expires_at = expires_at.decode('utf-8')
                if isinstance(expires_at, str):
                    if datetime.now() < datetime.fromisoformat(expires_at):
                        return token
    except sqlite3.Error as e:
        print(f"❌ Помилка отримання токена з сесії: {e}")
    return None


def clear_session():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sessions")
            conn.commit()
            print("🔒 Сесію завершено.")
    except sqlite3.Error as e:
        print(f"❌ Помилка завершення сесії: {e}")
