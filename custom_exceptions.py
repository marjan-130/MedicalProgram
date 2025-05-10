class EmptyFieldError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Помилка: {message}")

class ValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Помилка валідації: {message}")

class DatabaseConnectionError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Помилка підключення до БД: {message}")

class UserAlreadyExistsError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Користувач вже існує: {message}")

class IncorrectCredentialsError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Невірні дані для входу: {message}")