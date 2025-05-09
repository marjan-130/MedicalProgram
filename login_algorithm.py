import bcrypt
import sqlite3
from custom_exceptions import EmptyFieldError, ValidationError

def connect_to_database():
    """
    Підключення до SQLite-бази даних.
    """
    try:
        return sqlite3.connect('medical_program.db')
    except sqlite3.Error as e:
        raise Exception(f"Помилка підключення до бази даних: {e}")

def handle_login(username: str, password: str):
    """
    Обробка логіки входу користувача.

    :param username: Ім’я користувача
    :param password: Пароль
    :return: Дані користувача
    :raises EmptyFieldError: Якщо не всі поля заповнено
    :raises ValidationError: Якщо дані введено неправильно
    """
    if not username or not password:
        raise EmptyFieldError("Усі поля мають бути заповнені.")

    try:
        with connect_to_database() as conn:
            cursor = conn.cursor()

            # Отримуємо користувача за ім'ям користувача
            query = "SELECT id, user_name, hash_password, full_name, role FROM users WHERE user_name = ?"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if not user:
                raise ValidationError("Невірний логін або пароль.")

            # Перевіряємо, чи паролі збігаються
            if not bcrypt.checkpw(password.encode(), user[2].encode()):
                raise ValidationError("Невірний логін або пароль.")

            return user  # Повертаємо дані користувача

    except sqlite3.Error as e:
        raise Exception(f"Помилка бази даних: {e}")
