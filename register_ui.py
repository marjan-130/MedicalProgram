from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt
from register_algorithm import handle_register  # Логіка реєстрації
from custom_exceptions import EmptyFieldError, ValidationError  # Кастомні винятки



class BasicInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Реєстрація")
        self.setFixedSize(400, 650)  # Трохи зменшено висоту
        self.setStyleSheet("background-color: #f0f8ff; font-family: Arial;")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_widget = QWidget()
        form_widget.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
        """)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(12)

        title = QLabel("Реєстрація")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(title)

        # Стиль без проблем із обрізанням
        field_style = """
            background-color: #f5f5f5;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 14px;
            color: black;
        """
        combo_style = field_style

        def styled_line_edit(placeholder):
            le = QLineEdit()
            le.setPlaceholderText(placeholder)
            le.setFixedHeight(34)
            le.setStyleSheet(field_style)
            return le

        def styled_combo(items):
            cb = QComboBox()
            cb.addItems(items)
            cb.setFixedHeight(34)
            cb.setStyleSheet(combo_style)
            return cb

        self.username_input = styled_line_edit("Email")
        self.password_input = styled_line_edit("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password_input = styled_line_edit("Підтвердження паролю")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.full_name_input = styled_line_edit("Повне ім’я")
        self.birth_date_input = styled_line_edit("Дата народження (ДД/ММ/РРРР)")
        self.gender_input = styled_combo(["Чоловік", "Жінка", "Інше"])
        self.phone_input = styled_line_edit("Телефон")
        self.role_input = styled_combo(["Пацієнт", "Лікар"])

        next_button = QPushButton("Далі")
        next_button.setFixedHeight(40)
        next_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        next_button.setStyleSheet("""
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        """)
        next_button.clicked.connect(self.go_to_medical_info)

        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: red; font-size: 12px;")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        widgets = [
            self.username_input, self.password_input, self.confirm_password_input,
            self.full_name_input, self.birth_date_input, self.gender_input,
            self.phone_input, self.role_input, next_button, self.message_label
        ]
        for widget in widgets:
            form_layout.addWidget(widget)

        main_layout.addWidget(form_widget)
        self.setLayout(main_layout)

    def go_to_medical_info(self):
        try:
            username = self.username_input.text().strip()
            password = self.password_input.text().strip()
            confirm_password = self.confirm_password_input.text().strip()
            full_name = self.full_name_input.text().strip()
            birth_date = self.birth_date_input.text().strip()
            gender = self.gender_input.currentText().strip()
            phone = self.phone_input.text().strip()
            role = self.role_input.currentText().strip()

            if not all([username, password, full_name, birth_date, gender, phone, role]):
                raise EmptyFieldError("Усі поля повинні бути заповнені.")
            
            if password != confirm_password:
                raise ValidationError("Паролі не збігаються.")

            # Якщо валідація пройдена – перехід далі
            self.medical_info_window = MedicalInfoWindow(
                username, password, full_name, birth_date, gender, phone, role
            )
            self.medical_info_window.show()
            self.close()

        except EmptyFieldError as e:
            self.message_label.setText(str(e))
        except ValidationError as e:
            self.message_label.setText(str(e))
        except Exception as e:
            self.message_label.setText(f"Сталася помилка: {str(e)}")

class MedicalInfoWindow(QWidget):
    def __init__(self, username, password, full_name, birth_date, gender, phone, role):
        super().__init__()
        self.setWindowTitle("Медична інформація")
        self.setFixedSize(400, 600)
        self.setStyleSheet("""
            background-color: #f0f8ff;
            font-family: Arial;
        """)
        self.username = username
        self.password = password
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender
        self.phone = phone
        self.role = role
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_widget = QWidget()
        form_widget.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
        """)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(20)

        title = QLabel("Медична інформація")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(title)

        # Поля введення
        self.blood_type_input = QLineEdit()
        self.blood_type_input.setPlaceholderText("Тип крові (наприклад, A+, O-)")
        self.style_input(self.blood_type_input)

        self.chronic_diseases_input = QLineEdit()
        self.chronic_diseases_input.setPlaceholderText("Хронічні захворювання (якщо є)")
        self.style_input(self.chronic_diseases_input)

        self.allergies_input = QLineEdit()
        self.allergies_input.setPlaceholderText("Алергії (якщо є)")
        self.style_input(self.allergies_input)

        form_layout.addWidget(self.blood_type_input)
        form_layout.addWidget(self.chronic_diseases_input)
        form_layout.addWidget(self.allergies_input)

        # Повідомлення
        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: red;")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(self.message_label)

        # Кнопка
        register_button = QPushButton("Завершити реєстрацію")
        register_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        register_button.setFixedHeight(45)
        register_button.setStyleSheet("""
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: bold;
        """)
        register_button.clicked.connect(self.register)
        form_layout.addWidget(register_button)

        main_layout.addWidget(form_widget)
        self.setLayout(main_layout)

    def style_input(self, widget):
        widget.setFixedHeight(40)
        widget.setStyleSheet("""
            background-color: #f5f5f5;
            border: 1px solid #ccc;
            border-radius: 6px;
            padding-left: 10px;
            font-size: 14px;
            color: black;
        """)

    def register(self):
        blood_type = self.blood_type_input.text().strip()
        chronic_diseases = self.chronic_diseases_input.text().strip()
        allergies = self.allergies_input.text().strip()

        if not all([blood_type, chronic_diseases, allergies]):
            self.message_label.setText("Усі медичні поля повинні бути заповнені.")
        else:
            self.message_label.setStyleSheet("color: green;")
            self.message_label.setText("Реєстрація успішна!")
