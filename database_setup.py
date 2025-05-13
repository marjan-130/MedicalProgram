import os
import sqlite3

def create_database():
    db_path = 'medical_program.db'

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

            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT NOT NULL UNIQUE,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    expires_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                '''
                )

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    appointment_date DATE NOT NULL,
                    appointment_time TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (doctor_id) REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE(doctor_id, appointment_date, appointment_time)  -- уникаємо дублювань
                )
                ''')


            conn.commit()
            print(f"✅ Базу даних створено: {os.path.abspath(db_path)}")

    except sqlite3.Error as e:
        print(f"❌ Помилка при створенні бази даних: {e}")

create_database()
