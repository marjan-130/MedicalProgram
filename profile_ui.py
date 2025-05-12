from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QGridLayout, QWidget, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap, QLinearGradient, QPalette, QColor, QBrush
from PyQt6.QtCore import Qt
import sqlite3
from session import clear_session

class ProfileWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Профіль користувача")
        self.showMaximized()

        self.username = ""
        self.fields = {}
        self.labels = {}

        self.patient_fields = ["blood", "chronic", "allergies"]
        self.doctor_fields = ["specialization", "experience", "hospital"]

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_ui()
        self.load_user_data()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Встановлюємо фон
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 1000)
        gradient.setColorAt(0.0, QColor("#0d1b2a"))
        gradient.setColorAt(1.0, QColor("#1b263b"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.central_widget.setAutoFillBackground(True)
        self.central_widget.setPalette(palette)

        # Верхня панель
        self.top_bar = QHBoxLayout()
        self.welcome_label = QLabel("Welcome, ")
        self.welcome_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.welcome_label.setStyleSheet("color: white;")
        self.top_bar.addWidget(self.welcome_label)

        current_date = datetime.now().strftime("%a, %d %B %Y")
        self.date_label = QLabel(current_date)
        self.date_label.setFont(QFont("Arial", 12))
        self.date_label.setStyleSheet("color: white; margin-left: 10px;")
        self.top_bar.addWidget(self.date_label)

        self.top_bar.addStretch()

        self.edit_button = QPushButton("Edit")
        self.edit_button.setEnabled(False)
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #778da9;
                color: white;
                padding: 6px 12px;
                border-radius: 8px;
            }
        """)
        self.top_bar.addWidget(self.edit_button)

        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(50, 50)
        self.avatar_label.setPixmap(QPixmap("avatar.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.top_bar.addWidget(self.avatar_label)

        self.layout.addLayout(self.top_bar)

        # Секція профілю
        self.profile_section = QVBoxLayout()
        self.profile_section.setSpacing(30)

        self.name_label = QLabel("Ім’я Прізвище")
        self.name_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("color: white;")
        self.profile_section.addWidget(self.name_label)

        self.email_label = QLabel("email@example.com")
        self.email_label.setFont(QFont("Arial", 12))
        self.email_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.email_label.setStyleSheet("color: white;")
        self.profile_section.addWidget(self.email_label)

        self.form_layout = QGridLayout()
        self.form_layout.setSpacing(15)

        all_fields = {
            "full_name": "Full Name",
            "nickname": "Nick",
            "gender": "Gender",
            "birth_date": "Date",
            "phone": "Phone",
            "role": "Role",
            "blood": "Blood",
            "chronic": "Chronic Diseases",
            "allergies": "Allergies",
            "specialization": "Specialization",
            "experience": "Experience",
            "hospital": "Hospital",
        }

        for i, (key, placeholder) in enumerate(all_fields.items()):
            label = QLabel(key.capitalize())
            label.setStyleSheet("color: white;")
            field = QLineEdit()
            field.setPlaceholderText(placeholder)
            field.setReadOnly(True)
            field.setStyleSheet("""
                background-color: #f2f2f2;
                border-radius: 8px;
                padding: 8px;
                color: black;
            """)

            self.labels[key] = label
            self.fields[key] = field

            self.form_layout.addWidget(label, i // 2, (i % 2) * 2)
            self.form_layout.addWidget(field, i // 2, (i % 2) * 2 + 1)

        self.profile_section.addLayout(self.form_layout)
        self.layout.addLayout(self.profile_section)

        # Нижня панель з кнопками
        self.bottom_bar = QHBoxLayout()
        self.bottom_bar.addStretch()

        self.back_button = QPushButton("🔙 Назад у головне меню")
        self.back_button.setStyleSheet("background-color: #6c757d; color: white; padding: 8px 16px; border-radius: 8px;")
        self.back_button.clicked.connect(self.go_to_main_menu)
        self.bottom_bar.addWidget(self.back_button)

        self.logout_button = QPushButton("🚪 Вийти з акаунту")
        self.logout_button.setStyleSheet("background-color: #d62828; color: white; padding: 8px 16px; border-radius: 8px;")
        self.logout_button.clicked.connect(self.logout)
        self.bottom_bar.addWidget(self.logout_button)

        self.layout.addLayout(self.bottom_bar)

    def toggle_fields_visibility(self, visible_keys):
        for key in self.fields:
            is_visible = key in visible_keys
            self.fields[key].setVisible(is_visible)
            self.labels[key].setVisible(is_visible)

    def load_user_data(self):
        try:
            with sqlite3.connect("medical_program.db") as conn:
                cursor = conn.cursor()

                cursor.execute(''' 
                    SELECT u.user_name, i.full_name, i.birth_date, i.gender, i.email, i.phone, i.role,
                           i.blood_type, i.chronic_diseases, i.allergies,
                           d.specialization, d.experience, d.hospital
                    FROM users u
                    JOIN user_info i ON u.id = i.user_id
                    LEFT JOIN doctors d ON u.id = d.user_id
                    WHERE u.id = ?
                ''', (self.user_id,))
                data = cursor.fetchone()

                if data:
                    (username, full_name, birth_date, gender, email, phone, role,
                     blood, chronic, allergies, specialization, experience, hospital) = data

                    self.username = username
                    self.welcome_label.setText(f"Welcome, {username}")
                    self.name_label.setText(full_name)
                    self.email_label.setText(email)

                    self.fields["full_name"].setText(full_name or "")
                    self.fields["nickname"].setText(username or "")
                    self.fields["gender"].setText(gender or "")
                    self.fields["birth_date"].setText(birth_date or "")
                    self.fields["phone"].setText(phone or "")
                    self.fields["role"].setText(role or "")

                    if role == "пацієнт":
                        self.fields["blood"].setText(blood or "")
                        self.fields["chronic"].setText(chronic or "")
                        self.fields["allergies"].setText(allergies or "")
                        self.toggle_fields_visibility(
                            ["full_name", "nickname", "gender", "birth_date", "phone", "role"] + self.patient_fields
                        )
                    elif role == "лікар":
                        self.fields["specialization"].setText(specialization or "")
                        self.fields["experience"].setText(experience or "")
                        self.fields["hospital"].setText(hospital or "")
                        self.toggle_fields_visibility(
                            ["full_name", "nickname", "gender", "birth_date", "phone", "role"] + self.doctor_fields
                        )
                    else:
                        self.toggle_fields_visibility(
                            ["full_name", "nickname", "gender", "birth_date", "phone", "role"]
                        )
        except sqlite3.Error as e:
            print(f"Error loading user data: {e}")

    # Перехід назад
    def go_to_main_menu(self):
        self.close()
        from main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()

    def logout(self):
        confirm = QMessageBox.question(
            self, "Вийти",
            "Ви дійсно хочете вийти з акаунту?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            clear_session(self.user_id)
            self.close()

            from main_window import MainWindow
            self.main_window = MainWindow()
            self.main_window.show()