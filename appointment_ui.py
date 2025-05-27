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
        self.date_edit.setMinimumDate(today)

        self.available_dates = self.get_available_dates()
        if self.available_dates:
            self.date_edit.setDate(self.available_dates[0])
            self.date_edit.setMinimumDate(self.available_dates[0])
            self.date_edit.setMaximumDate(self.available_dates[-1])
        else:
            QMessageBox.information(self, "Немає доступу", "У цьому місяці немає доступних днів.")
            self.setDisabled(True)

        self.layout.addWidget(self.date_edit)

        self.time_box = QComboBox()
        self.layout.addWidget(self.time_box)

        self.book_button = QPushButton("Записатись")
        self.book_button.clicked.connect(self.book_appointment)
        self.layout.addWidget(self.book_button)

        self.setLayout(self.layout)

        self.date_edit.dateChanged.connect(self.update_time_slots)
        self.update_time_slots()

    def get_doctor_id(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT d.id FROM doctors d
                JOIN user_info ui ON d.user_info_id = ui.id
                WHERE ui.full_name = ?
            ''', (self.doctor_name,))
            row = cursor.fetchone()
            return row[0] if row else None

    def get_available_dates(self):
        doctor_id = self.get_doctor_id()
        if not doctor_id:
            return []

        today = datetime.date.today()
        last_day = datetime.date(today.year, today.month, QDate(today.year, today.month, 1).daysInMonth())
        available = []

        for offset in range((last_day - today).days + 1):
            day = today + datetime.timedelta(days=offset)
            if day.weekday() > 4:
                continue
            slots = self.get_all_slots_for_day(day)
            booked = self.get_booked_slots(doctor_id, day)
            if len(booked) < len(slots):
                available.append(QDate(day.year, day.month, day.day))
        return available

    def get_all_slots_for_day(self, date):
        weekday = date.weekday()
        slots = []
        if weekday in [0, 2, 4]:
            hours = range(9, 13)
        elif weekday in [1, 3]:
            hours = range(15, 19)
        else:
            return []

        for h in hours:
            for m in [0, 20, 40]:
                slots.append(f"{h:02d}:{m:02d}")
        return slots

    def get_booked_slots(self, doctor_id, date):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT appointment_time FROM appointments
                WHERE doctor_id = ? AND appointment_date = ?
            ''', (doctor_id, date.strftime("%Y-%m-%d")))
            return [row[0] for row in cursor.fetchall()]

    def update_time_slots(self):
        self.time_box.clear()
        date = self.date_edit.date().toPyDate()
        doctor_id = self.get_doctor_id()
        if not doctor_id:
            return

        all_slots = self.get_all_slots_for_day(date)
        booked_slots = self.get_booked_slots(doctor_id, date)
        free_slots = [slot for slot in all_slots if slot not in booked_slots]

        if not free_slots:
            self.time_box.addItem("Немає доступного часу")
            self.book_button.setDisabled(True)
        else:
            self.time_box.addItems(free_slots)
            self.book_button.setEnabled(True)

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

        doctor_id = self.get_doctor_id()
        if not doctor_id:
            QMessageBox.critical(self, "Помилка", "Лікаря не знайдено.")
            return

        date_qdate = self.date_edit.date()
        date_str = date_qdate.toString("yyyy-MM-dd")
        time_str = self.time_box.currentText()

        if time_str == "Немає доступного часу":
            QMessageBox.warning(self, "Зайнято", "Цей день повністю зайнятий.")
            return

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id FROM appointments
                WHERE doctor_id = ? AND appointment_date = ? AND appointment_time = ?
            ''', (doctor_id, date_str, time_str))
            if cursor.fetchone():
                QMessageBox.warning(self, "Зайнято", "Цей час вже зайнятий.")
                self.update_time_slots()
                return

            cursor.execute('''
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time)
                VALUES (?, ?, ?, ?)
            ''', (patient_id, doctor_id, date_str, time_str))
            conn.commit()
            QMessageBox.information(self, "Успішно", "Запис створено!")
            self.close()
