import os
import sqlite3

def create_database():
    db_path = 'medical_program.db'
    conn = sqlite3.connect(db_path)
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
            birth_date TEXT,
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
            specialization TEXT,
            experience TEXT,
            hospital TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print(f"✅ Базу даних створено: {os.path.abspath(db_path)}")

create_database()
