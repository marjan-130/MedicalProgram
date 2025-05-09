from PyQt6.QtWidgets import QApplication, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QThread, pyqtSignal
from DataBase import connect_to_database
from login_ui import LoginWindow  # Імпорт LoginWindow


class DbConnectionThread(QThread):
    """Потік для підключення до бази даних в окремому потоці."""
    result = pyqtSignal(object)

    def run(self):
        """Спробує підключитись до бази даних і поверне результат через сигнал."""
        try:
            connection = connect_to_database()
            self.result.emit(connection if connection else None)
        except Exception as e:
            self.result.emit(str(e))


def handle_button_click(text: str, window):
    """Обробляє натискання кнопок на головному вікні."""
    if text == "Enter":
        # Інформаційне повідомлення для кнопки "Enter"
        QMessageBox.information(window, "Info", "Enter pressed (без підключення до БД)")
    elif text == "Exit":
        # Закриває програму при натисканні на кнопку "Exit"
        QApplication.quit()
    elif text == "Login":
        # Відкриває вікно входу при натисканні на кнопку "Login"
        window.login_window = LoginWindow(window.login_success)
        window.login_window.show()


def on_db_connection_result(connection, window):
    """Обробляє результат підключення до бази даних та відображає дані."""
    if isinstance(connection, str):
        # Якщо підключення не вдалося, виводимо повідомлення про помилку
        QMessageBox.critical(window, "Error", f"DB Error: {connection}")
    elif connection:
        try:
            # Отримуємо курсор для виконання запитів
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM login")
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            if not results:
                # Якщо дані відсутні в таблиці
                QMessageBox.warning(window, "Warning", "No data found in the database.")
                return

            # Створюємо таблицю для відображення даних
            table = QTableWidget()
            table.setRowCount(len(results))
            table.setColumnCount(len(columns))
            table.setHorizontalHeaderLabels(columns)

            for row_idx, row in enumerate(results):
                for col_idx, value in enumerate(row):
                    table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            # Автоматично змінюємо розмір стовпців та налаштовуємо розміри вікна
            table.resizeColumnsToContents()
            table.resize(600, 400)
            table.setWindowTitle("Users Table")
            table.show()

            window.table_window = table
        except Exception as e:
            # Якщо сталася помилка при роботі з базою даних
            QMessageBox.critical(window, "Error", f"An error occurred: {str(e)}")
        finally:
            # Закриваємо підключення до бази даних
            connection.close()
    else:
        # Якщо неможливо підключитись до бази даних
        QMessageBox.warning(window, "Warning", "Unable to connect to the database.")
