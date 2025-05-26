import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QMessageBox, QPushButton, QHBoxLayout
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QLinearGradient, QColor, QFont
from PyQt6.QtCore import Qt
from datetime import datetime, timedelta  # ДОДАНО timedelta

DB_PATH = 'medical_program.db'


class ReminderCard(QFrame):
    def __init__(self, icon_path, title, details: list[str], button_text, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("background-color: white; border-radius: 16px;")
        self.setMinimumHeight(160)

        icon_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(64, 64)

        text_layout = QVBoxLayout()
        title_label = QLabel(f"<b>{title}</b>")
        title_label.setFont(QFont("Segoe UI", 16))
        title_label.setStyleSheet("color: #023047;")
        text_layout.addWidget(title_label)
        for line in details:
            lbl = QLabel(line)
            lbl.setFont(QFont("Segoe UI", 13))
            lbl.setStyleSheet("color: #03045e;")
            text_layout.addWidget(lbl)
        text_layout.addStretch()

        button = QPushButton(button_text)
        button.setFixedSize(120, 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #a2d2ff;
                color: black;
            }
        """)
        button.clicked.connect(lambda: QMessageBox.information(self, "Дія", f"Виконано: {button_text}"))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(24)
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(button)


class ReminderWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Мої нагадування")
        self.resize(700, 800)
        self.setup_ui()

    def setup_ui(self):
        # Градієнтний фон
        palette = QPalette()
        grad = QLinearGradient(0, 0, 0, 1)
        grad.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)
        grad.setColorAt(0.0, QColor("#a2d2ff"))
        grad.setColorAt(1.0, QColor("#d0f4ff"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(grad))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(24)

        header = QLabel("МОЇ НАГАДУВАННЯ")
        header.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #03045e;")
        main_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidgetResizable(True)
        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setSpacing(20)

        self.load_appointments(vbox)
        self.load_medicines(vbox)

        vbox.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def load_appointments(self, layout):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT d.specialization, ui.full_name, a.appointment_date, a.appointment_time
                    FROM appointments a
                    JOIN doctors d ON a.doctor_id = d.id
                    JOIN user_info ui ON d.user_info_id = ui.id
                    WHERE a.patient_id = (
                        SELECT id FROM user_info WHERE user_id = ?
                    )
                    AND date(a.appointment_date) >= date('now')
                    ORDER BY a.appointment_date ASC
                ''', (self.user_id,))
                rows = cursor.fetchall()
                for spec, doctor_name, date_, time_ in rows:
                    layout.addWidget(ReminderCard(
                        icon_path="pictures/doctor_icon.png",
                        title="Прийом до лікаря",
                        details=[
                            f"Лікар: {doctor_name} ({spec})",
                            f"Дата: {date_}",
                            f"Час: {time_}"
                        ],
                        button_text="Переглянути"
                    ))
        except sqlite3.Error as e:
            print(f"❌ Помилка завантаження прийомів: {e}")

    def load_medicines(self, layout):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                today = datetime.now().date()
                cursor.execute('''
                    SELECT name, start_date, times_per_day, duration_days, first_dose_time
                    FROM medicines
                    WHERE user_id = ?
                ''', (self.user_id,))
                rows = cursor.fetchall()
                for name, start_date, times_per_day, duration_days, first_time in rows:
                    start = datetime.fromisoformat(start_date).date()
                    end = start + timedelta(days=duration_days)
                    if start <= today <= end:
                        times = self.calculate_times(first_time, times_per_day)
                        layout.addWidget(ReminderCard(
                            icon_path="pictures/pill_icon.png",
                            title="Прийом ліків",
                            details=[
                                f"Ліки: {name}",
                                f"Дозування: {times_per_day} рази/день",
                                f"Час: {', '.join(times)}"
                            ],
                            button_text="Прийняти"
                        ))
        except sqlite3.Error as e:
            print(f"❌ Помилка завантаження ліків: {e}")

    def calculate_times(self, first_time_str, times_per_day):
        first_time = datetime.strptime(first_time_str, "%H:%M")
        interval = 24 // times_per_day
        times = [(first_time + timedelta(hours=i * interval)).strftime("%H:%M") for i in range(times_per_day)]
        return times
