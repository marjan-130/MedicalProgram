from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QComboBox, 
                           QSpinBox, QTimeEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import QDate
import sqlite3

class MedicineDialog(QDialog):
    def __init__(self, date: QDate, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Додати ліки")
        self.date = date
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Назва ліків")
        
        self.times_per_day = QComboBox()
        self.times_per_day.addItems(["1 раз на день", "2 рази на день", "3 рази на день", "4 рази на день"])
        
        self.duration = QSpinBox()
        self.duration.setRange(1, 365)
        self.duration.setSuffix(" днів")
        
        self.first_dose = QTimeEdit()
        self.first_dose.setDisplayFormat("HH:mm")
        
        layout.addRow("Назва ліків:", self.name_input)
        layout.addRow("Кількість прийомів:", self.times_per_day)
        layout.addRow("Тривалість:", self.duration)
        layout.addRow("Перший прийом:", self.first_dose)
        
        save_btn = QPushButton("Зберегти")
        save_btn.clicked.connect(self.save_medicine)
        layout.addRow(save_btn)

    def save_medicine(self):
        name = self.name_input.text()
        if not name:
            QMessageBox.warning(self, "Помилка", "Введіть назву ліків")
            return
            
        times = int(self.times_per_day.currentText().split()[0])
        duration = self.duration.value()
        first_dose = self.first_dose.time().toString("HH:mm")
        
        try:
            with sqlite3.connect('medical_program.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO medicines (user_id, name, start_date, times_per_day, 
                                          duration_days, first_dose_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (self.parent().user_id, name, self.date.toString("yyyy-MM-dd"), 
                     times, duration, first_dose))
                conn.commit()
                
            QMessageBox.information(self, "Успіх", "Ліки успішно додані")
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти: {e}")
