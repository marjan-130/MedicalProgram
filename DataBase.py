# -*- coding: utf-8 -*-
import sqlite3

# Функція для підключення до бази даних
def connect_to_database():
    try:
        conn = sqlite3.connect('medical_program.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Функція для вставки нового користувача
def add_user(user_name, hash_password):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        
        # Виконання запиту на вставку даних
        cursor.execute('''
            INSERT INTO users (user_name, hash_password)
            VALUES (?, ?)
        ''', (user_name, hash_password))
        
        # Підтвердження змін та закриття з'єднання
        conn.commit()
        conn.close()
        print(f"User '{user_name}' added successfully.")
    else:
        print("Unable to connect to the database.")

# Функція для отримання всіх користувачів
def get_all_users():
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    return []

