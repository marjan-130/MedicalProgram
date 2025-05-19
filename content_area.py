from PyQt6.QtWidgets import (QScrollArea, QWidget, QVBoxLayout, QLabel, 
                           QFrame, QHBoxLayout, QPushButton, QSizePolicy)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
import os
import sqlite3
from calendar_widget import CalendarWidget
from session import get_session_user_id

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
        
        self.user_id = getattr(parent, 'user_id', None)

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

        doctor_info = QVBoxLayout()
        doctor_info.setSpacing(5)

        pib_label = QLabel("ПІБ")
        pib_label.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 600;
            color: #8a94a6;
            font-size: 12px;
        """)

        doctor_name = QLabel("-")
        doctor_name.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 700;
            color: white;
            font-size: 16px;
        """)

        doctor_info.addWidget(pib_label)
        doctor_info.addWidget(doctor_name)

        spec_layout = QVBoxLayout()
        spec_layout.setSpacing(5)

        spec_label = QLabel("Спеціалізація")
        spec_label.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 600;
            color: #8a94a6;
            font-size: 12px;
        """)

        spec_value = QLabel("-")
        spec_value.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 700;
            color: white;
            font-size: 14px;
        """)

        spec_layout.addWidget(spec_label)
        spec_layout.addWidget(spec_value)

        date_layout = QVBoxLayout()
        date_layout.setSpacing(5)

        date_label = QLabel("Дата")
        date_label.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 600;
            color: #8a94a6;
            font-size: 12px;
            text-align: right;
        """)
        date_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        date_value = QLabel("-")
        date_value.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 700;
            color: white;
            font-size: 14px;
            text-align: right;
        """)
        date_value.setAlignment(Qt.AlignmentFlag.AlignRight)

        date_layout.addWidget(date_label)
        date_layout.addWidget(date_value)

        visit_card_layout.addWidget(avatar)
        visit_card_layout.addLayout(doctor_info, 1)
        visit_card_layout.addLayout(spec_layout, 1)
        visit_card_layout.addLayout(date_layout, 1)

        visits_layout.addWidget(visit_card)
        self.content_layout.addWidget(visits_container)

        try:
            with sqlite3.connect('medical_program.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT a.appointment_date, a.appointment_time, ui.full_name, d.specialization
                    FROM appointments a
                    JOIN doctors d ON a.doctor_id = d.user_id
                    JOIN user_info ui ON d.user_id = ui.user_id
                    WHERE a.patient_id = ?
                    ORDER BY a.appointment_date ASC, a.appointment_time ASC
                    LIMIT 1
                ''', (self.user_id,))

                result = cursor.fetchone()
                if result:
                    appointment_date, time, name, specialization = result
                    doctor_name.setText(name)
                    spec_value.setText(specialization)
                    date_value.setText(f"{appointment_date}, {time}")
        except sqlite3.Error as e:
            print(f"Помилка завантаження найближчого візиту: {e}")

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

        self.calendar_widget = CalendarWidget(self.user_id)
        calendar_layout.addWidget(self.calendar_widget)

        self.content_layout.addWidget(calendar_container)