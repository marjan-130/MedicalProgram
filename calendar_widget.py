from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                           QPushButton, QCalendarWidget, QMessageBox)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QTextCharFormat, QColor
import sqlite3
from medicine_dialog import MedicineDialog
from session import is_session_active, get_session_user_id

class CalendarWidget(QWidget):
    def __init__(self, user_id=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id or get_session_user_id()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
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

        self.meds_label = QLabel("Ліки:")
        self.meds_label.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 600;
            color: white;
            font-size: 16px;
            margin-top: 20px;
        """)

        self.meds_list = QVBoxLayout()
        self.meds_list.setSpacing(10)

        self.visits_label = QLabel("Записи до лікаря:")
        self.visits_label.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 600;
            color: white;
            font-size: 16px;
            margin-top: 20px;
        """)

        self.visits_list = QVBoxLayout()
        self.visits_list.setSpacing(10)

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
        info_layout.addWidget(self.meds_label)
        info_layout.addLayout(self.meds_list)
        info_layout.addWidget(self.visits_label)
        info_layout.addLayout(self.visits_list)
        info_layout.addWidget(add_medicine_btn)
        info_layout.addStretch()

        layout.addWidget(self.calendar, 2)
        layout.addWidget(self.info_panel, 1)

        self.on_date_selected(QDate.currentDate())
        self.highlight_medicine_days()

    def highlight_medicine_days(self):
        if not is_session_active():
            return
        user_id = self.user_id or get_session_user_id()
        if not user_id:
            return

        try:
            with sqlite3.connect('medical_program.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT start_date, duration_days 
                    FROM medicines
                    WHERE user_id = ?
                ''', (user_id,))
                dates = cursor.fetchall()

                fmt = QTextCharFormat()
                fmt.setBackground(QColor("#FFD966"))

                self.calendar.setDateTextFormat(QDate(), QTextCharFormat())

                for start_date_str, duration_days in dates:
                    start_date = QDate.fromString(start_date_str, "yyyy-MM-dd")
                    for i in range(duration_days):
                        day = start_date.addDays(i)
                        self.calendar.setDateTextFormat(day, fmt)
        except sqlite3.Error as e:
            print(f"Помилка підсвітки днів ліків: {e}")

    def on_date_selected(self, date):
        self.current_date = date
        self.date_label.setText(date.toString("dddd, dd MMMM yyyy"))

        for layout in (self.meds_list, self.visits_list):
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        self.load_events(date)
        self.highlight_medicine_days()

    def load_events(self, date):
        date_str = date.toString("yyyy-MM-dd")
        has_events = False

        try:
            with sqlite3.connect('medical_program.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT name, times_per_day, first_dose_time 
                    FROM medicines 
                    WHERE user_id = ? AND start_date <= ? 
                    AND date(start_date, '+' || duration_days || ' days') >= ?
                ''', (self.user_id, date_str, date_str))

                for name, times, first_dose in cursor.fetchall():
                    has_events = True
                    event = QLabel(f"💊 {name} - {times} раз(и) на день, перший прийом о {first_dose}")
                    event.setStyleSheet("color: #8a94a6; font-size: 14px;")
                    self.meds_list.addWidget(event)
        except sqlite3.Error as e:
            print(f"Помилка завантаження ліків: {e}")

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
                    has_events = True
                    event = QLabel(f"👨‍⚕️ {time} - {doctor} ({specialization})")
                    event.setStyleSheet("color: #8a94a6; font-size: 14px;")
                    self.visits_list.addWidget(event)
        except sqlite3.Error as e:
            print(f"Помилка завантаження записів: {e}")

        if not has_events:
            no_events = QLabel("Немає подій на цей день")
            no_events.setStyleSheet("color: #8a94a6; font-style: italic;")
            self.meds_list.addWidget(no_events)

    def add_medicine(self):
        if not is_session_active():
            QMessageBox.warning(self, "Помилка", "Увійдіть в систему для додавання ліків")
            return

        user_id = get_session_user_id()
        if not user_id:
            QMessageBox.warning(self, "Помилка", "Сесія недійсна або завершена")
            return

        dialog = MedicineDialog(date=self.current_date, user_id=user_id, parent=self)
        if dialog.exec():
            self.on_date_selected(self.current_date)