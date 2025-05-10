import bcrypt
import sqlite3
from custom_exceptions import EmptyFieldError, ValidationError

def connect_to_database():
    try:
        return sqlite3.connect('medical_program.db')
    except sqlite3.Error as e:
        raise Exception(f"Помилка підключення до бази даних: {e}")

def handle_login(username: str, password: str):
    # Перевірка на пусті поля
    if not username or not password:
        raise EmptyFieldError("Усі поля мають бути заповнені.")

    try:
        with connect_to_database() as conn:
            cursor = conn.cursor()

            # Запит для пошуку користувача за логіном
            query = """
            SELECT users.id, users.user_name, users.hash_password,
                   user_info.full_name, users.role
            FROM users
            LEFT JOIN user_info ON users.id = user_info.user_id
            WHERE users.user_name = ?
            """
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if not user:
                raise ValidationError("Невірний логін або пароль.")  # Користувача не знайдено

            # Перевірка пароля
            if not bcrypt.checkpw(password.encode(), user[2].encode()):
                raise ValidationError("Невірний логін або пароль.")  # Невірний пароль

            return user  # Повертаємо дані користувача, якщо успішна авторизація

    except sqlite3.Error as e:
        raise Exception(f"Помилка бази даних: {e}")  # Помилка під час роботи з базою
