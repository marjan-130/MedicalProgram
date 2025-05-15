import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QDateEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate

DB_PATH = 'medical_program.db'

class AppointmentWidget(QWidget):
    def __init__(self, doctor_name, user_id):  # Додано doctor_name
        super().__init__()
        self.doctor_name = doctor_name  # Зберігаємо ім'я лікаря
        self.user_id = user_id  # Зберігаємо user_id
        self.setWindowTitle(f"Запис до лікаря {self.doctor_name}")

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(f"Виберіть дату та час для лікаря {self.doctor_name}:"))

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.layout.addWidget(self.date_edit)

        self.time_box = QComboBox()
        self.layout.addWidget(self.time_box)

        self.book_button = QPushButton("Записатись")
        self.book_button.clicked.connect(self.book_appointment)
        self.layout.addWidget(self.book_button)

        self.setLayout(self.layout)

        self.date_edit.dateChanged.connect(self.update_time_slots)
        self.update_time_slots()

    # Тут можна прибрати load_doctors(), doctor_box, бо лікар передається явно
    # А також поправити book_appointment, щоб використовував self.doctor_name чи інший унікальний ідентифікатор лікаря
    
    def update_time_slots(self):
        self.time_box.clear()
        date = self.date_edit.date().toPyDate()
        weekday = date.weekday()

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

        # Для запису потрібен doctor_id, тому треба отримати його за іменем лікаря
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

            date_str = self.date_edit.date().toString("yyyy-MM-dd")
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
