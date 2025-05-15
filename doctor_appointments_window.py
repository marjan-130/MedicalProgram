import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt

DB_PATH = 'medical_program.db'

class DoctorAppointmentsWindow(QWidget):
    def __init__(self, doctor_user_id):
        super().__init__()
        self.setWindowTitle("Записи пацієнтів")
        self.resize(600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Список записів пацієнтів:")
        self.layout.addWidget(self.label)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.doctor_user_id = doctor_user_id
        self.load_appointments()

    def load_appointments(self):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                # Отримати doctor.id через user_info та user_id
                cursor.execute('''
                    SELECT d.id FROM doctors d
                    JOIN user_info ui ON d.user_info_id = ui.id
                    WHERE ui.user_id = ?
                ''', (self.doctor_user_id,))
                doctor_row = cursor.fetchone()

                if not doctor_row:
                    QMessageBox.critical(self, "Помилка", "Лікаря не знайдено.")
                    return

                doctor_id = doctor_row[0]

                # Витягнути записи
                cursor.execute('''
                    SELECT ui.full_name, a.appointment_date, a.appointment_time
                    FROM appointments a
                    JOIN user_info ui ON a.patient_id = ui.id
                    WHERE a.doctor_id = ?
                    ORDER BY a.appointment_date, a.appointment_time
                ''', (doctor_id,))
                records = cursor.fetchall()

                self.table.setRowCount(len(records))
                self.table.setColumnCount(3)
                self.table.setHorizontalHeaderLabels(["Пацієнт", "Дата", "Час"])
                self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

                for row_idx, (name, date, time) in enumerate(records):
                    self.table.setItem(row_idx, 0, QTableWidgetItem(name))
                    self.table.setItem(row_idx, 1, QTableWidgetItem(date))
                    self.table.setItem(row_idx, 2, QTableWidgetItem(time))

                self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Помилка", str(e))
