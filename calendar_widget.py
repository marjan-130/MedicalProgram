from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                           QPushButton, QCalendarWidget, QMessageBox)
from PyQt6.QtCore import QDate, Qt
import sqlite3
from medicine_dialog import MedicineDialog

class CalendarWidget(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Календар
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #041e49;
                color: white;
            }
            QCalendarWidget QToolButton {
                color: white;
                font-size: 14px;
            }
            QCalendarWidget QMenu {
                background-color: #041e49;
                color: white;
            }
        """)
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.on_date_selected)
        
        # Інформаційна панель
        self.info_panel = QWidget()
        self.info_panel.setStyleSheet("""
            background-color: #0a285c;
            border-radius: 15px;
            padding: 15px;
        """)
        info_layout = QVBoxLayout(self.info_panel)
        
        self.date_label = QLabel()
        self.date_label.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 700;
            color: white;
            font-size: 20px;
        """)
        
        self.events_label = QLabel("Події:")
        self.events_label.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 600;
            color: white;
            font-size: 16px;
            margin-top: 20px;
        """)
        
        self.events_list = QVBoxLayout()
        self.events_list.setSpacing(10)
        
        add_medicine_btn = QPushButton("Додати ліки")
        add_medicine_btn.setStyleSheet("""
            QPushButton {
                background-color: #66BFFF;
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #55AAEE;
            }
        """)
        add_medicine_btn.clicked.connect(self.add_medicine)
        
        info_layout.addWidget(self.date_label)
        info_layout.addWidget(self.events_label)
        info_layout.addLayout(self.events_list)
        info_layout.addWidget(add_medicine_btn)
        info_layout.addStretch()
        
        layout.addWidget(self.calendar, 2)
        layout.addWidget(self.info_panel, 1)
        
        # Оновлюємо відображення для поточної дати
        self.on_date_selected(QDate.currentDate())

    def on_date_selected(self, date):
        self.current_date = date
        self.date_label.setText(date.toString("dddd, dd MMMM yyyy"))
        
        # Очищаємо попередні події
        while self.events_list.count():
            item = self.events_list.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Завантажуємо події для вибраної дати
        self.load_events(date)

    def load_events(self, date):
        date_str = date.toString("yyyy-MM-dd")
        
        # Завантажуємо ліки
        try:
            with sqlite3.connect('medical_program.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT name, times_per_day, first_dose_time 
                    FROM medicines 
                    WHERE user_id = ? AND start_date <= ? 
                    AND date(?, '+' || duration_days || ' days') >= start_date
                ''', (self.user_id, date_str, date_str))
                
                for name, times, first_dose in cursor.fetchall():
                    event = QLabel(f"💊 {name} - {times} раз(и) на день, перший прийом о {first_dose}")
                    event.setStyleSheet("color: #8a94a6; font-size: 14px;")
                    self.events_list.addWidget(event)
        except sqlite3.Error as e:
            print(f"Помилка завантаження ліків: {e}")
        
        # Завантажуємо записи до лікаря
        try:
            with sqlite3.connect('medical_program.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT a.appointment_time, ui.full_name, d.specialization
                    FROM appointments a
                    JOIN doctors d ON a.doctor_id = d.user_id
                    JOIN user_info ui ON d.user_id = ui.user_id
                    WHERE a.patient_id = ? AND a.appointment_date = ?
                ''', (self.user_id, date_str))
                
                for time, doctor, specialization in cursor.fetchall():
                    event = QLabel(f"👨‍⚕️ {time} - {doctor} ({specialization})")
                    event.setStyleSheet("color: #8a94a6; font-size: 14px;")
                    self.events_list.addWidget(event)
        except sqlite3.Error as e:
            print(f"Помилка завантаження записів: {e}")
        
        if self.events_list.count() == 0:
            no_events = QLabel("Немає подій на цей день")
            no_events.setStyleSheet("color: #8a94a6; font-style: italic;")
            self.events_list.addWidget(no_events)

    def add_medicine(self):
        if not self.user_id:
            QMessageBox.warning(self, "Помилка", "Увійдіть в систему для додавання ліків")
            return
            
        dialog = MedicineDialog(self.current_date, self)
        if dialog.exec():
            self.update_events()