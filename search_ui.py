import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QScrollArea, QTabWidget
)
from PyQt6.QtCore import Qt
import sys


class DoctorCard(QWidget):
    def __init__(self, name, specialty, hospital, times):
        super().__init__()
        layout = QVBoxLayout()

        # Інформація про лікаря
        layout.addWidget(QLabel(f"<b>{name}</b>"))
        layout.addWidget(QLabel(specialty))
        layout.addWidget(QLabel(hospital))

        # Години запису
        time_layout = QHBoxLayout()
        for time in times:
            btn = QPushButton(time)
            btn.setStyleSheet("""
                background-color: #e6f0ff;
                border: none;
                border-radius: 10px;
                padding: 6px 12px;
            """)
            time_layout.addWidget(btn)

        layout.addLayout(time_layout)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        self.setLayout(layout)
        self.setStyleSheet("""
            background-color: white;
            border-radius: 16px;
        """)

        self.setFixedSize(300, 150)


class DoctorSearchTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
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

        # Пошуковий блок
        search_layout = QHBoxLayout()
        self.combo_specialty = QComboBox()
        self.combo_specialty.addItem("Усі спеціальності")
        self.combo_specialty.addItems(["Сімейний лікар", "Терапевт", "Педіатр"])
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введіть прізвище або спеціальність")
        search_button = QPushButton("Знайти")
        search_button.clicked.connect(self.load_doctors_from_db)

        search_layout.addWidget(self.combo_specialty)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        # Банер
        banner = QLabel("👨‍⚕️ <b>ЛІКАР</b> — Ми знайдемо для вас ідеального лікаря")
        banner.setStyleSheet("""
            background-color: #e6f9e6;
            padding: 12px;
            border-radius: 12px;
        """)

        # Список лікарів
        self.doctor_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background: transparent;")
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.doctor_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        # Компоновка
        main_layout.addLayout(search_layout)
        main_layout.addWidget(banner)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.load_doctors_from_db()


    def load_doctors_from_db(self):
        # Очистити попередній вміст
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
            self.doctor_layout.addWidget(QLabel("Лікарів не знайдено."))
            return

        for doc in doctors:
            name, specialty, hospital = doc
            times = ["09:00", "11:30", "14:00"]  # Якщо буде таблиця з годинами — додамо динамічно
            card = DoctorCard(name, specialty, hospital, times)
            self.doctor_layout.addWidget(card)