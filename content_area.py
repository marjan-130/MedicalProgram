from PyQt6.QtWidgets import (QScrollArea, QWidget, QVBoxLayout, QLabel,
                             QFrame, QHBoxLayout, QPushButton, QSizePolicy)
from PyQt6.QtGui import QIcon, QFont, QPalette, QBrush, QLinearGradient, QColor
from PyQt6.QtCore import Qt, QSize
import os
import sqlite3
from calendar_widget import CalendarWidget


class ContentArea(QScrollArea):
    def __init__(self, user_id=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id

        self.setWidgetResizable(True)
        self.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background: transparent;
            }
            QScrollBar:vertical { 
                width: 8px; 
                background: rgba(2, 48, 71, 0.1);
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(2, 48, 71, 0.3);
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(25)

        self._setup_header()
        self._setup_upcoming_visit()
        self._setup_calendar_section()

        self.setWidget(self.content_widget)

    def resizeEvent(self, event):
        # Оновлюємо градієнт при зміні розміру
        self.update_gradient()
        super().resizeEvent(event)

    def update_gradient(self):
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#a2d2ff"))  # Дуже світлий блакитний
        gradient.setColorAt(1.0, QColor("#d0f4ff"))  # Трохи темніший блакитний
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def _setup_header(self):
        title = QLabel("Панель здоров'я")
        title.setStyleSheet("""
            font-family: 'Segoe UI';
            font-weight: 700;
            color: #023047;
            font-size: 28px;
            margin-bottom: 10px;
        """)
        self.content_layout.addWidget(title)

    def _setup_upcoming_visit(self):
        visits_container = QFrame()
        visits_container.setStyleSheet("""
            background-color: white;
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(2, 48, 71, 0.1);
        """)
        visits_layout = QVBoxLayout(visits_container)
        visits_layout.setContentsMargins(0, 0, 0, 0)
        visits_layout.setSpacing(15)

        header_layout = QHBoxLayout()

        visit_title = QLabel("Найближчий візит")
        visit_title.setStyleSheet("""
            font-family: 'Segoe UI';
            font-weight: 700;
            color: #023047;
            font-size: 20px;
        """)

        all_visits_btn = QPushButton("Всі візити →")
        all_visits_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        all_visits_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #2196F3;
                font-family: 'Segoe UI';
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
            background-color: #e3f2fd;
            border-radius: 12px;
            padding: 15px;
            border: 1px solid rgba(2, 48, 71, 0.1);
        """)
        visit_card.setMinimumHeight(80)

        visit_card_layout = QHBoxLayout(visit_card)
        visit_card_layout.setContentsMargins(15, 15, 15, 15)
        visit_card_layout.setSpacing(10)

        avatar = QLabel()
        avatar.setFixedSize(50, 50)
        avatar.setStyleSheet("""
            background-color: #bbdefb;
            border-radius: 25px;
        """)

        avatar_path = "img/user.svg"
        if os.path.exists(avatar_path):
            avatar.setPixmap(QIcon(avatar_path).pixmap(QSize(30, 30)))

        visit_card_layout.addWidget(avatar)

        self.visit_info_label = QLabel("-")
        self.visit_info_label.setStyleSheet("""
            font-family: 'Segoe UI';
            font-weight: 700;
            color: #023047;
            font-size: 16px;
            padding-left: 15px;
        """)
        self.visit_info_label.setWordWrap(True)
        visit_card_layout.addWidget(self.visit_info_label)

        visits_layout.addWidget(visit_card)
        self.content_layout.addWidget(visits_container)

        if self.user_id is None:
            self.visit_info_label.setText("Користувач не знайдений")
            return

        try:
            with sqlite3.connect('medical_program.db') as conn:
                cursor = conn.cursor()

                cursor.execute(""" 
                    SELECT a.appointment_date, a.appointment_time, d.specialization, di.full_name
                    FROM appointments a
                    JOIN doctors d ON a.doctor_id = d.id
                    JOIN user_info di ON d.user_info_id = di.id
                    WHERE a.patient_id = (SELECT id FROM user_info WHERE user_id = ?)
                    AND date(a.appointment_date) >= date('now')
                    ORDER BY a.appointment_date ASC, a.appointment_time ASC
                    LIMIT 1
                """, (self.user_id,))

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
            background-color: white;
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(2, 48, 71, 0.1);
        """)
        calendar_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        calendar_layout = QVBoxLayout(calendar_container)
        calendar_layout.setContentsMargins(0, 0, 0, 0)

        calendar_title = QLabel("Календар")
        calendar_title.setStyleSheet("""
            font-family: 'Segoe UI';
            font-weight: 700;
            color: #023047;
            font-size: 20px;
        """)
        calendar_layout.addWidget(calendar_title)

        self.calendar_widget = CalendarWidget()
        calendar_layout.addWidget(self.calendar_widget)

        self.content_layout.addWidget(calendar_container)