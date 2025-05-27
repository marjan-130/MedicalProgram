from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                             QPushButton, QCalendarWidget, QMessageBox)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QTextCharFormat, QColor, QFont
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
        background-color: white;
        border-radius: 16px;
        padding: 15px;
    }
    QCalendarWidget QToolButton {
        color: #023047;
        font-size: 14px;
        font-weight: 600;
    }
    QCalendarWidget QMenu {
        background-color: white;
        color: #023047;
    }
    QCalendarWidget QSpinBox {
        background-color: white;
        color: #023047;
    }
    QCalendarWidget QWidget { 
        alternate-background-color: white; 
    }
    /* Додайте ці нові стилі */
    QCalendarWidget QAbstractItemView:enabled {
        color: #023047;  /* Колір тексту днів */
        font-size: 14px;
        font-weight: 500;
        selection-background-color: #a2d2ff;
        selection-color: #023047;
    }
""")
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.on_date_selected)
        
        self.info_panel = QWidget()
        self.info_panel.setStyleSheet("""
            background-color: white;
            border-radius: 16px;
            padding: 15px;
        """)
        info_layout = QVBoxLayout(self.info_panel)

        self.date_label = QLabel()
        self.date_label.setStyleSheet("""
            font-family: 'Segoe UI';
            font-weight: 700;
            color: #023047;
            font-size: 20px;
        """)

        self.meds_label = QLabel("Ліки:")
        self.meds_label.setStyleSheet("""
            font-family: 'Segoe UI';
            font-weight: 600;
            color: #023047;
            font-size: 16px;
            margin-top: 20px;
        """)

        self.meds_list = QVBoxLayout()
        self.meds_list.setSpacing(10)

        self.visits_label = QLabel("Записи до лікаря:")
        self.visits_label.setStyleSheet("""
            font-family: 'Segoe UI';
            font-weight: 600;
            color: #023047;
            font-size: 16px;
            margin-top: 20px;
        """)

        self.visits_list = QVBoxLayout()
        self.visits_list.setSpacing(10)

        add_medicine_btn = QPushButton("Додати ліки")
        add_medicine_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                padding: 8px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #43a047;
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
        self.highlight_days()

    def highlight_days(self):
        if not is_session_active():
            return
        user_id = self.user_id or get_session_user_id()
        if not user_id:
            return

        try:
            with sqlite3.connect('medical_program.db') as conn:
                cursor = conn.cursor()

                # Отримуємо дати з ліками
                cursor.execute('''
                    SELECT start_date, duration_days
                    FROM medicines
                    WHERE user_id = ?
                ''', (user_id,))
                meds_dates_raw = cursor.fetchall()

                meds_dates = set()
                for start_date_str, duration_days in meds_dates_raw:
                    start_date = QDate.fromString(start_date_str, "yyyy-MM-dd")
                    for i in range(duration_days):
                        meds_dates.add(start_date.addDays(i))

                # Отримуємо дати з візитами до лікаря
                cursor.execute('''
                    SELECT DISTINCT appointment_date
                    FROM appointments
                    WHERE patient_id = ?
                ''', (user_id,))
                visits_dates_raw = cursor.fetchall()

                visits_dates = set()
                for (date_str,) in visits_dates_raw:
                    visits_dates.add(QDate.fromString(date_str, "yyyy-MM-dd"))

                # Очищаємо всі підсвітки
                self.calendar.setDateTextFormat(QDate(), QTextCharFormat())

                yellow_fmt = QTextCharFormat()
                yellow_fmt.setBackground(QColor("#FFD966"))  # жовтий
                yellow_fmt.setForeground(QColor("#023047"))  # темно-синій текст

                green_fmt = QTextCharFormat()
                green_fmt.setBackground(QColor("#6CCC5A"))  # зелений
                green_fmt.setForeground(QColor("#023047"))  # темно-синій текст
                purple_fmt = QTextCharFormat()
                purple_fmt.setBackground(QColor("#9b59b6"))  # фіолетовий
                purple_fmt.setForeground(QColor("023047"))  # білий текст для контрасту
              

                # Об'єднуємо всі дати для підсвітки
                all_dates = meds_dates.union(visits_dates)

                for day in all_dates:
                    has_meds = day in meds_dates
                    has_visits = day in visits_dates
                    if has_meds and has_visits:
                        self.calendar.setDateTextFormat(day, purple_fmt)
                    elif has_meds:
                        self.calendar.setDateTextFormat(day, yellow_fmt)
                    elif has_visits:
                        self.calendar.setDateTextFormat(day, green_fmt)

        except sqlite3.Error as e:
            print(f"Помилка підсвітки днів: {e}")

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
        self.highlight_days()

    def load_events(self, date):
        date_str = date.toString("yyyy-MM-dd")

        meds_found = False
        visits_found = False

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
                    meds_found = True
                    event = QLabel(f"💊 {name} - {times} раз(и) на день, перший прийом о {first_dose}")
                    event.setStyleSheet("color: #8a94a6; font-size: 14px;")
                    self.meds_list.addWidget(event)
        except sqlite3.Error as e:
            print(f"Помилка завантаження ліків: {e}")

        if not meds_found:
            no_meds = QLabel("Немає ліків на цей день")
            no_meds.setStyleSheet("color: #8a94a6; font-style: italic;")
            self.meds_list.addWidget(no_meds)

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
                    visits_found = True
                    event = QLabel(f"👨‍⚕️ {time} - {doctor} ({specialization})")
                    event.setStyleSheet("color: #8a94a6; font-size: 14px;")
                    self.visits_list.addWidget(event)
        except sqlite3.Error as e:
            print(f"Помилка завантаження записів: {e}")

        if not visits_found:
            no_visits = QLabel("Немає записів до лікаря на цей день")
            no_visits.setStyleSheet("color: #8a94a6; font-style: italic;")
            self.visits_list.addWidget(no_visits)

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
