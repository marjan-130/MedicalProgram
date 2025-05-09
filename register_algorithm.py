import bcrypt
import sqlite3
from custom_exceptions import EmptyFieldError, ValidationError

def handle_register(username, password, confirm_password, full_name, birth_date, gender, email, phone, role, blood_type, chronic_diseases, allergies, medications):
    """
    Обробка логіки реєстрації нового користувача.

    :raises EmptyFieldError: Якщо не заповнено обов'язкові поля.
    :raises ValidationError: Якщо паролі не збігаються або користувач вже існує.
    """

    if not username or not password or not confirm_password or not full_name or not birth_date or not gender or not email or not phone or not blood_type:
        raise EmptyFieldError("Будь ласка, заповніть усі обов'язкові поля.")
    
    if password != confirm_password:
        raise ValidationError("Паролі не співпадають.")
    
    conn = None
    try:
        conn = sqlite3.connect('medical_program.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE user_name = ?", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            raise ValidationError("Користувач з таким іменем вже існує.")
        
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

        cursor.execute("INSERT INTO users (user_name, hash_password) VALUES (?, ?)", (username, hashed_password))
        user_id = cursor.lastrowid

        cursor.execute(''' 
            INSERT INTO user_info (
                user_id, full_name, birth_date, gender, email, phone,
                role, blood_type, chronic_diseases, allergies, medications
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, full_name, birth_date, gender, email, phone,
            role, blood_type, chronic_diseases, allergies, medications
        ))

        conn.commit()
    except sqlite3.Error as e:
        raise Exception(f"Помилка бази даних: {e}")
    finally:
        if conn:
            conn.close()
