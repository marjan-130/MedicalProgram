from PyQt6.QtWidgets import (QScrollArea, QWidget, QVBoxLayout, QLabel,
                             QFrame, QHBoxLayout, QPushButton, QSizePolicy)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
import os
import sqlite3
from calendar_widget import CalendarWidget


class ContentArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background-color: #021a43;
            }
            QScrollBar:vertical { 
                width: 8px; 
                background: #051e4a;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #0a285c;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(25)

        self._setup_header()
        self._setup_upcoming_visit()
        self._setup_calendar_section()

        self.setWidget(self.content_widget)

    def _setup_header(self):
        title = QLabel("Панель здоров'я")
        title.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 700;
            color: white;
            font-size: 28px;
            margin-bottom: 10px;
        """)
        self.content_layout.addWidget(title)

    def _setup_upcoming_visit(self):
        visits_container = QFrame()
        visits_container.setStyleSheet("""
            background-color: #0a285c;
            border-radius: 15px;
        """)
        visits_layout = QVBoxLayout(visits_container)
        visits_layout.setContentsMargins(25, 20, 25, 20)
        visits_layout.setSpacing(15)

        header_layout = QHBoxLayout()

        visit_title = QLabel("Найближчий візит")
        visit_title.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 700;
            color: white;
            font-size: 20px;
        """)

        all_visits_btn = QPushButton("Всі візити →")
        all_visits_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        all_visits_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-family: 'Inter';
                font-weight: 600;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)

        header_layout.addWidget(visit_title)
        header_layout.addStretch()
        header_layout.addWidget(all_visits_btn)

        visits_layout.addLayout(header_layout)

        visit_card = QFrame()
        visit_card.setStyleSheet("""
            background-color: #041e49;
            border-radius: 12px;
            padding: 15px;
        """)
        visit_card.setMinimumHeight(80)

        visit_card_layout = QHBoxLayout(visit_card)
        visit_card_layout.setContentsMargins(15, 15, 15, 15)
        visit_card_layout.setSpacing(10)

        avatar = QLabel()
        avatar.setFixedSize(50, 50)
        avatar.setStyleSheet("""
            background-color: #0a285c;
            border-radius: 25px;
        """)

        avatar_path = "img/user.svg"
        if os.path.exists(avatar_path):
            avatar.setPixmap(QIcon(avatar_path).pixmap(QSize(30, 30)))

        visit_card_layout.addWidget(avatar)

        self.visit_info_label = QLabel("-")
        self.visit_info_label.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 700;
            color: white;
            font-size: 16px;
            padding-left: 15px;
        """)
        self.visit_info_label.setWordWrap(True)
        visit_card_layout.addWidget(self.visit_info_label)

        visits_layout.addWidget(visit_card)
        self.content_layout.addWidget(visits_container)

        # Отримуємо user_id безпосередньо з бази
        try:
            with sqlite3.connect('medical_program.db') as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT user_id FROM user_info LIMIT 1")
                row = cursor.fetchone()
                if not row:
                    self.visit_info_label.setText("Користувач не знайдений")
                    return
                current_user_id = row[0]

                cursor.execute("""
                    SELECT a.appointment_date, a.appointment_time, d.specialization, di.full_name
                    FROM appointments a
                    JOIN doctors d ON a.doctor_id = d.id
                    JOIN user_info di ON d.user_info_id = di.id
                    WHERE a.patient_id = (SELECT id FROM user_info WHERE user_id = ?)
                    AND date(a.appointment_date) >= date('now')
                    ORDER BY a.appointment_date ASC, a.appointment_time ASC
                    LIMIT 1
                """, (current_user_id,))

                result = cursor.fetchone()
                if result:
                    appointment_date, appointment_time, specialization, doctor_name = result
                    self.visit_info_label.setText(
                        f"{doctor_name} – {specialization} – {appointment_date}, {appointment_time}"
                    )
                else:
                    self.visit_info_label.setText("Немає запланованих візитів")

        except sqlite3.Error as e:
            print(f"Помилка завантаження найближчого візиту: {e}")
            self.visit_info_label.setText("Помилка завантаження візиту")

    def _setup_calendar_section(self):
        calendar_container = QFrame()
        calendar_container.setStyleSheet("""
            background-color: #0a285c;
            border-radius: 15px;
        """)
        calendar_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        calendar_layout = QVBoxLayout(calendar_container)
        calendar_layout.setContentsMargins(25, 20, 25, 20)

        calendar_title = QLabel("Календар")
        calendar_title.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 700;
            color: white;
            font-size: 20px;
        """)
        calendar_layout.addWidget(calendar_title)

        self.calendar_widget = CalendarWidget()
        calendar_layout.addWidget(self.calendar_widget)

        self.content_layout.addWidget(calendar_container)
