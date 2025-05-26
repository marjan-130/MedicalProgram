import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QDateEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate
import datetime

DB_PATH = 'medical_program.db'

class AppointmentWidget(QWidget):
    def __init__(self, doctor_name, user_id):
        super().__init__()
        self.doctor_name = doctor_name
        self.user_id = user_id
        self.setWindowTitle(f"Запис до лікаря {self.doctor_name}")

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(f"Виберіть дату та час для лікаря {self.doctor_name}:"))

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        today = QDate.currentDate()
        self.date_edit.setDate(today)

        # Забороняємо минулі дати
        self.date_edit.setMinimumDate(today)

        # Обмеження лише поточним місяцем
        last_day = QDate(today.year(), today.month(), today.daysInMonth())
        self.date_edit.setMaximumDate(last_day)

        self.layout.addWidget(self.date_edit)

        self.time_box = QComboBox()
        self.layout.addWidget(self.time_box)

        self.book_button = QPushButton("Записатись")
        self.book_button.clicked.connect(self.book_appointment)
        self.layout.addWidget(self.book_button)

        self.setLayout(self.layout)

        self.date_edit.dateChanged.connect(self.update_time_slots)
        self.update_time_slots()

    def update_time_slots(self):
        self.time_box.clear()
        date = self.date_edit.date().toPyDate()
        weekday = date.weekday()

        # Тільки будні дні (Пн–Пт)
        if weekday > 4:
            return

        slots = []
        if weekday in [0, 2, 4]:  # Пн, Ср, Пт
            hours = range(9, 13)
        elif weekday in [1, 3]:  # Вт, Чт
            hours = range(15, 19)
        else:
            return

        for h in hours:
            for m in [0, 20, 40]:
                slots.append(f"{h:02d}:{m:02d}")

        self.time_box.addItems(slots)

    def get_patient_id(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id FROM user_info
                WHERE user_id = ? AND role = 'пацієнт'
            ''', (self.user_id,))
            row = cursor.fetchone()
            return row[0] if row else None

    def book_appointment(self):
        patient_id = self.get_patient_id()
        if not patient_id:
            QMessageBox.critical(self, "Помилка", "Сесія недійсна або ви не пацієнт.")
            return

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT d.id FROM doctors d
                JOIN user_info ui ON d.user_info_id = ui.id
                WHERE ui.full_name = ?
            ''', (self.doctor_name,))
            doctor_row = cursor.fetchone()
            if not doctor_row:
                QMessageBox.critical(self, "Помилка", "Лікаря не знайдено.")
                return
            doctor_id = doctor_row[0]

            date_qdate = self.date_edit.date()
            date_py = date_qdate.toPyDate()
            today = datetime.date.today()

            #  Заборонити минулі дати
            if date_py < today:
                QMessageBox.warning(self, "Недійсна дата", "Неможливо записатися на минулу дату.")
                return

            #  Заборонити запис не на поточний місяць
            if date_py.month != today.month or date_py.year != today.year:
                QMessageBox.warning(self, "Недійсна дата", "Запис доступний лише на поточний місяць.")
                return

            #  Заборонити запис у вихідні
            if date_py.weekday() > 4:
                QMessageBox.warning(self, "Недійсний день", "Запис можливий лише в будні дні.")
                return

            date_str = date_qdate.toString("yyyy-MM-dd")
            time_str = self.time_box.currentText()

            cursor.execute('''
                SELECT id FROM appointments
                WHERE doctor_id = ? AND appointment_date = ? AND appointment_time = ?
            ''', (doctor_id, date_str, time_str))
            if cursor.fetchone():
                QMessageBox.warning(self, "Зайнято", "Цей час вже зайнятий.")
                return

            cursor.execute('''
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time)
                VALUES (?, ?, ?, ?)
            ''', (patient_id, doctor_id, date_str, time_str))
            conn.commit()
            QMessageBox.information(self, "Успішно", "Запис створено!")
            self.close()