import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox, QFormLayout, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class EmptyFieldError(Exception):
    """Виключення для порожніх полів."""
    pass

class RegisterUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Реєстрація")
        self.setFixedSize(400, 600)
        self.setStyleSheet("background-color: #f0f8ff; font-family: Arial;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form = QWidget()
        form.setStyleSheet("background-color: white; border-radius: 15px;")
        form_layout = QVBoxLayout(form)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(20)

        title = QLabel("Реєстрація")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(title)

        self.username_input = self.create_field("Логін")
        self.password_input = self.create_field("Пароль", is_password=True)
        self.full_name_input = self.create_field("ПІБ")
        self.birth_date_input = self.create_field("Дата народження")
        self.gender_input = self.create_combo_box(["Чоловік", "Жінка"])
        self.phone_input = self.create_field("Телефон")
        self.role_input = self.create_combo_box(["Пацієнт", "Лікар"])

        for widget in [self.username_input, self.password_input, self.full_name_input,
                       self.birth_date_input, self.gender_input, self.phone_input, self.role_input]:
            form_layout.addWidget(widget)

        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: red;")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(self.message_label)

        register_button = QPushButton("Перейти до медичної інформації")
        register_button.setFixedHeight(45)
        register_button.setStyleSheet(
            "background-color: #007bff; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: bold;"
        )
        register_button.clicked.connect(self.register)
        form_layout.addWidget(register_button)

        layout.addWidget(form)
        self.setLayout(layout)

    def create_field(self, placeholder, is_password=False):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setEchoMode(QLineEdit.EchoMode.Password if is_password else QLineEdit.EchoMode.Normal)
        field.setFixedHeight(40)
        field.setStyleSheet(
            "background-color: #f5f5f5; border: 1px solid #ccc; border-radius: 6px; padding-left: 10px; font-size: 14px; color: black;"
        )
        return field

    def create_combo_box(self, items):
        combo_box = QComboBox()
        combo_box.addItems(items)
        combo_box.setFixedHeight(40)
        combo_box.setStyleSheet(
            "background-color: #f5f5f5; border: 1px solid #ccc; border-radius: 6px; font-size: 14px;"
        )
        return combo_box

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        full_name = self.full_name_input.text().strip()
        birth_date = self.birth_date_input.text().strip()
        gender = self.gender_input.currentText()
        phone = self.phone_input.text().strip()
        role = self.role_input.currentText().lower()

        try:
            if not all([username, password, full_name, birth_date, gender, phone, role]):
                raise EmptyFieldError("Будь ласка, заповніть усі поля.")

            user_id = self.save_user_data(username, password, full_name, birth_date, gender, phone, role)

            if role == "пацієнт":
                self.show_patient_form(user_id)
            else:
                self.show_doctor_form(user_id)

        except EmptyFieldError as e:
            self.message_label.setText(str(e))
        except sqlite3.IntegrityError:
            self.message_label.setText("Користувач з таким логіном вже існує.")
        except Exception as e:
            self.message_label.setText(f"Помилка: {e}")

    def save_user_data(self, username, password, full_name, birth_date, gender, phone, role):
        conn = sqlite3.connect('medical_program.db', timeout=10)
        cursor = conn.cursor()

        # Додаємо користувача до таблиці users
        cursor.execute('''
            INSERT INTO users (user_name, hash_password)
            VALUES (?, ?)
        ''', (username, password))

        # Отримуємо user_id новоствореного користувача
        cursor.execute('SELECT id FROM users WHERE user_name = ?', (username,))
        user_id = cursor.fetchone()[0]

        # Додаємо основну інформацію користувача до user_info
        cursor.execute('''
            INSERT INTO user_info (user_id, full_name, birth_date, gender, phone, role)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, full_name, birth_date, gender, phone, role))

        conn.commit()
        conn.close()
        return user_id

    def show_patient_form(self, user_id):
        form = QDialog()
        form_layout = QFormLayout()

        blood_type_input = self.create_field("Група крові")
        chronic_diseases_input = self.create_field("Хронічні захворювання")
        allergies_input = self.create_field("Алергії")

        save_button = QPushButton("Зберегти")
        save_button.clicked.connect(lambda: (
            self.save_patient_data(user_id, blood_type_input.text(), chronic_diseases_input.text(), allergies_input.text()),
            form.accept()
        ))

        form_layout.addRow("Група крові:", blood_type_input)
        form_layout.addRow("Хронічні захворювання:", chronic_diseases_input)
        form_layout.addRow("Алергії:", allergies_input)
        form_layout.addWidget(save_button)

        form.setLayout(form_layout)
        form.setWindowTitle("Медична інформація пацієнта")
        form.exec()

    def save_patient_data(self, user_id, blood_type, chronic_diseases, allergies):
        conn = sqlite3.connect('medical_program.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE user_info
            SET blood_type = ?, chronic_diseases = ?, allergies = ?
            WHERE user_id = ?
        ''', (blood_type, chronic_diseases, allergies, user_id))
        conn.commit()
        conn.close()

    def show_doctor_form(self, user_id):
        form = QDialog()
        form_layout = QFormLayout()

        specialization_input = self.create_field("Спеціалізація")
        experience_input = self.create_field("Досвід роботи")
        hospital_input = self.create_field("Лікарня")

        save_button = QPushButton("Зберегти")
        save_button.clicked.connect(lambda: (
            self.save_doctor_data(user_id, specialization_input.text(), experience_input.text(), hospital_input.text()),
            form.accept()
        ))

        form_layout.addRow("Спеціалізація:", specialization_input)
        form_layout.addRow("Досвід роботи:", experience_input)
        form_layout.addRow("Лікарня:", hospital_input)
        form_layout.addWidget(save_button)

        form.setLayout(form_layout)
        form.setWindowTitle("Інформація лікаря")
        form.exec()

    def save_doctor_data(self, user_id, specialization, experience, hospital):
        conn = sqlite3.connect('medical_program.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO doctors (user_id, specialization, experience, hospital)
            VALUES (?, ?, ?, ?)
        ''', (user_id, specialization, experience, hospital))
        conn.commit()
        conn.close()
