import sqlite3
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QScrollArea
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from appointment_ui import AppointmentWidget


class DoctorCard(QWidget):
    def __init__(self, name, specialty, hospital, photo_path=None, parent=None):
        super().__init__()

        self.parent_tab = parent  # Зберігаємо об'єкт батьківського класу (DoctorSearchTab)

        card_layout = QHBoxLayout()
        card_layout.setContentsMargins(12, 8, 12, 8)

        # Фото лікаря
        photo_label = QLabel()
        pixmap = QPixmap("pictures/default_doctor.png")
        pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        photo_label.setPixmap(pixmap)
        photo_label.setFixedSize(80, 80)

        # Текстова інформація
        text_layout = QVBoxLayout()
        name_label = QLabel(f"<b>{name}</b>")
        specialty_label = QLabel(specialty)
        hospital_label = QLabel(hospital)

        for label in [name_label, specialty_label, hospital_label]:
            label.setStyleSheet("background: transparent; color: black; font-size: 18px;")

        text_layout.addWidget(name_label)
        text_layout.addWidget(specialty_label)
        text_layout.addWidget(hospital_label)
        text_layout.setSpacing(4)

        info_layout = QVBoxLayout()
        info_layout.addLayout(text_layout)
        info_layout.setSpacing(6)

        # Кнопка "Записатись"
        book_button = QPushButton("Записатись")
        book_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        book_button.setFixedHeight(40)
        book_button.setFixedWidth(120)
        book_button.clicked.connect(lambda: self.parent_tab.book_appointment(name))  # Викликаємо метод через parent_tab

        card_layout.addWidget(photo_label)
        card_layout.addLayout(info_layout)
        card_layout.addStretch()
        card_layout.addWidget(book_button)

        self.setLayout(card_layout)
        self.setStyleSheet("""
            border-radius: 14px;
            background: white;
        """)
        self.setFixedHeight(130)
        self.setMinimumWidth(620)


class DoctorSearchTab(QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id  # Збереження user_id поточного користувача
        self.showFullScreen()

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #0066cc,
                    stop: 1 #99ccff
                );
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 40, 20, 20)

        # Пошуковий рядок
        search_layout = QHBoxLayout()

        # Кнопка Назад
        back_button = QPushButton("← Назад")
        back_button.setFixedWidth(100)
        back_button.setStyleSheet("font-size: 16px; padding: 6px 12px;")

        self.combo_specialty = QComboBox()
        self.combo_specialty.addItem("Усі спеціальності")
        self.combo_specialty.addItems([
            "Терапевт", "Кардіолог", "Педіатр", "Хірург", "Невролог",
            "Дерматолог", "Гінеколог", "Офтальмолог", "Отоларинголог", "Онколог"
        ])
        self.combo_specialty.setStyleSheet("font-size: 16px;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введіть прізвище або спеціальність")
        self.search_input.setStyleSheet("font-size: 16px; padding: 6px;")

        search_button = QPushButton("Знайти")
        search_button.setStyleSheet("font-size: 16px; padding: 6px 20px;")
        search_button.clicked.connect(self.load_doctors_from_db)

        search_layout.addWidget(back_button)
        search_layout.addWidget(self.combo_specialty)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        # Банер
        banner = QLabel("👨‍⚕️ <b>ЛІКАР</b> — Ми знайдемо для вас ідеального лікаря")
        banner.setStyleSheet("""
            background-color: #e6f9e6;
            padding: 14px;
            border-radius: 12px;
            font-size: 20px;
        """)

        # Область прокрутки для карток лікарів
        self.doctor_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background: transparent")
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.doctor_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        main_layout.addLayout(search_layout)
        main_layout.addWidget(banner)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.load_doctors_from_db()

    def load_doctors_from_db(self):
        while self.doctor_layout.count():
            child = self.doctor_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        cursor = self.db.cursor()

        specialty_filter = self.combo_specialty.currentText()
        search_text = self.search_input.text().strip().lower()

        query = '''
            SELECT
                ui.full_name,
                d.specialization,
                d.hospital
            FROM doctors d
            JOIN user_info ui ON d.user_id = ui.user_id
        '''

        filters = []
        params = []

        if specialty_filter != "Усі спеціальності":
            filters.append("d.specialization = ?")
            params.append(specialty_filter)

        if search_text:
            filters.append("LOWER(ui.full_name) LIKE ?")
            params.append(f"%{search_text}%")

        if filters:
            query += " WHERE " + " AND ".join(filters)

        cursor.execute(query, params)
        doctors = cursor.fetchall()

        if not doctors:
            not_found = QLabel("Лікарів не знайдено.")
            not_found.setStyleSheet("font-size: 18px; color: white;")
            self.doctor_layout.addWidget(not_found)
            return

        for doc in doctors:
            name, specialty, hospital = doc
            photo_path = "default_doctor.png"
            card = DoctorCard(name, specialty, hospital, photo_path, parent=self)
            self.doctor_layout.addWidget(card)

    def book_appointment(self, doctor_name):
        # Передаємо user_id разом з іменем лікаря в AppointmentWidget
        self.appointment_window = AppointmentWidget(doctor_name, self.user_id)
        self.appointment_window.show()
