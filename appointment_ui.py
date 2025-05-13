import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QDateEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate
from datetime import datetime

DB_PATH = 'medical_program.db'

class AppointmentWidget(QWidget):
    def __init__(self, session_token):
        super().__init__()
        self.session_token = session_token
        self.setWindowTitle("Запис до лікаря")

        self.layout = QVBoxLayout()

        self.label = QLabel("Виберіть дату та час:")
        self.layout.addWidget(self.label)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.layout.addWidget(self.date_edit)

        self.time_box = QComboBox()
        self.layout.addWidget(self.time_box)

        self.doctor_box = QComboBox()
        self.layout.addWidget(QLabel("Лікар:"))
        self.layout.addWidget(self.doctor_box)

        self.book_button = QPushButton("Записатись")
        self.book_button.clicked.connect(self.book_appointment)
        self.layout.addWidget(self.book_button)

        self.setLayout(self.layout)

        self.date_edit.dateChanged.connect(self.update_time_slots)
        self.load_doctors()
        self.update_time_slots()

    def load_doctors(self):
        self.doctor_box.clear()
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT d.id, ui.full_name
                FROM doctors d
                JOIN user_info ui ON d.user_info_id = ui.id
            ''')
            for doc_id, name in cursor.fetchall():
                self.doctor_box.addItem(name, doc_id)

    def update_time_slots(self):
        self.time_box.clear()
        date = self.date_edit.date().toPyDate()
        weekday = date.weekday()  # 0 = Пн, 6 = Нд

        slots = []
        if weekday in [0, 2, 4]:  # Пн, Ср, Пт
            start_hour, end_hour = 9, 13
        elif weekday in [1, 3]:  # Вт, Чт
            start_hour, end_hour = 15, 19
        else:
            return

        for h in range(start_hour, end_hour):
            for m in [0, 20, 40]:
                slots.append(f"{h:02d}:{m:02d}")

        self.time_box.addItems(slots)

    def get_patient_id(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT u.id FROM users u
                JOIN sessions s ON s.user_id = u.id
                JOIN user_info ui ON ui.user_id = u.id
                WHERE s.session_token = ? AND ui.role = 'пацієнт'
            ''', (self.session_token,))
            row = cursor.fetchone()
            return row[0] if row else None

    def book_appointment(self):
        patient_id = self.get_patient_id()
        if not patient_id:
            QMessageBox.critical(self, "Помилка", "Сесія недійсна або ви не пацієнт.")
            return

        doctor_id = self.doctor_box.currentData()
        date_str = self.date_edit.date().toString("yyyy-MM-dd")
        time_str = self.time_box.currentText()

        # Перевірка зайнятості
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id FROM appointments
                WHERE doctor_id = ? AND appointment_date = ? AND appointment_time = ?
            ''', (doctor_id, date_str, time_str))
            if cursor.fetchone():
                QMessageBox.warning(self, "Зайнято", "Цей час вже зайнятий.")
                return

            # Запис
            cursor.execute('''
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time)
                VALUES (?, ?, ?, ?)
            ''', (patient_id, doctor_id, date_str, time_str))
            conn.commit()
            QMessageBox.information(self, "Успішно", "Запис створено!")

