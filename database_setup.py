# -*- coding: utf-8 -*-
import sqlite3

# Функція для створення бази даних та таблиці
def create_database():
    # Підключення до бази даних
    conn = sqlite3.connect('medical_program.db')
    
    # Створення курсора для виконання SQL запитів
    cursor = conn.cursor()
    
    # Створення таблиці, якщо вона не існує
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            hash_password TEXT NOT NULL
        )
    ''')
    
    # Підтвердження змін та закриття з'єднання
    conn.commit()
    conn.close()
    print("Database and table created successfully.")

# Викликаємо функцію для створення бази даних
create_database()
