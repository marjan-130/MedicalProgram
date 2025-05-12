import json
import os
from datetime import datetime, timedelta

# Зберігаємо файл сесії в домашній директорії користувача
SESSION_FILE = os.path.join(os.path.expanduser("~"), "session.json")
SESSION_DURATION = timedelta(hours=24)

def create_session(user_id: int):
    session_data = {
        "user_id": user_id,
        "login_time": datetime.now().isoformat()
    }
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump(session_data, f)
    except Exception as e:
        print(f"Failed to create session: {e}")

def get_session():
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE, "r") as f:
            session_data = json.load(f)
        login_time = datetime.fromisoformat(session_data.get("login_time", ""))
        if datetime.now() - login_time < SESSION_DURATION:
            return session_data.get("user_id")
    except Exception as e:
        print(f"Failed to read session: {e}")
    return None

def clear_session():
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
    except Exception as e:
        print(f"Failed to clear session: {e}")

def get_session_user_id():
    user_id = get_session()
    return user_id if user_id is not None else None

def is_session_active():
    return get_session() is not None

def refresh_session():
    user_id = get_session_user_id()
    if user_id:
        create_session(user_id)
