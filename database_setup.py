import os
import sqlite3

def create_database():
    db_path = 'medical_program.db'

    # Перевірка наявності бази даних
    if os.path.exists(db_path):
        print(f"⚠️ База даних вже існує: {os.path.abspath(db_path)}")
        return

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Увімкнення підтримки зовнішніх ключів
            cursor.execute("PRAGMA foreign_keys = ON")

            # Таблиця користувачів (логін та пароль)
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL UNIQUE,
                    hash_password TEXT NOT NULL
                )
            ''')

            # Таблиця з персональною, контактною та медичною інформацією
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    full_name TEXT,
                    birth_date DATE,
                    gender TEXT,
                    email TEXT,
                    phone TEXT,
                    role TEXT CHECK(role IN ('пацієнт', 'лікар')) DEFAULT 'пацієнт',
                    blood_type TEXT,
                    chronic_diseases TEXT,
                    allergies TEXT,
                    medications TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')

            # Таблиця з додатковою інформацією про лікаря
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS doctors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    user_info_id INTEGER NOT NULL,  -- Зовнішній ключ до user_info
                    specialization TEXT,
                    experience TEXT,
                    hospital TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_info_id) REFERENCES user_info(id) ON DELETE CASCADE
                )
            ''')

            conn.commit()
            print(f"✅ Базу даних створено: {os.path.abspath(db_path)}")

    except sqlite3.Error as e:
        print(f"❌ Помилка при створенні бази даних: {e}")

create_database()
