import sqlite3
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QScrollArea
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from appointment_ui import AppointmentWidget


class DoctorCard(QWidget):
    def __init__(self, name, specialty, hospital, photo_path=None, parent=None):
        super().__init__()

        self.parent_tab = parent

        card_layout = QHBoxLayout()
        card_layout.setContentsMargins(12, 8, 12, 8)

        photo_label = QLabel()
        pixmap = QPixmap("pictures/default_doctor.png")
        pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        photo_label.setPixmap(pixmap)
        photo_label.setFixedSize(80, 80)

        text_layout = QVBoxLayout()
        name_label = QLabel(f"<b>{name}</b>")
        specialty_label = QLabel(specialty)
        hospital_label = QLabel(hospital)

        for label in [name_label, specialty_label, hospital_label]:
            label.setStyleSheet("background: transparent; color: black; font-size: 18px;")

        text_layout.addWidget(name_label)
        text_layout.addWidget(specialty_label)
        text_layout.addWidget(hospital_label)
        text_layout.setSpacing(4)

        info_layout = QVBoxLayout()
        info_layout.addLayout(text_layout)
        info_layout.setSpacing(6)

        book_button = QPushButton("\u0417\u0430\u043f\u0438\u0441\u0430\u0442\u0438\u0441\u044c")
        book_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        book_button.setFixedHeight(40)
        book_button.setFixedWidth(120)
        book_button.clicked.connect(lambda: self.parent_tab.book_appointment(name))

        card_layout.addWidget(photo_label)
        card_layout.addLayout(info_layout)
        card_layout.addStretch()
        card_layout.addWidget(book_button)

        self.setLayout(card_layout)
        self.setStyleSheet("""
            border-radius: 14px;
            background: white;
        """)
        self.setFixedHeight(130)
        self.setMinimumWidth(620)


class DoctorSearchTab(QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.showFullScreen()

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #0066cc,
                    stop: 1 #99ccff
                );
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 40, 20, 20)

        search_layout = QHBoxLayout()

        back_button = QPushButton("\u2190 \u041d\u0430\u0437\u0430\u0434")
        back_button.setFixedWidth(100)
        back_button.setStyleSheet("font-size: 16px; padding: 6px 12px;")
        back_button.clicked.connect(self.go_back_to_main)

        self.combo_specialty = QComboBox()
        self.combo_specialty.addItem("\u0423\u0441\u0456 \u0441\u043f\u0435\u0446\u0456\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u0456")
        self.combo_specialty.addItems([
            "\u0422\u0435\u0440\u0430\u043f\u0435\u0432\u0442", "\u041a\u0430\u0440\u0434\u0456\u043e\u043b\u043e\u0433", "\u041f\u0435\u0434\u0456\u0430\u0442\u0440", "\u0425\u0456\u0440\u0443\u0440\u0433", "\u041d\u0435\u0432\u0440\u043e\u043b\u043e\u0433",
            "\u0414\u0435\u0440\u043c\u0430\u0442\u043e\u043b\u043e\u0433", "\u0413\u0456\u043d\u0435\u043a\u043e\u043b\u043e\u0433", "\u041e\u0444\u0442\u0430\u043b\u044c\u043c\u043e\u043b\u043e\u0433", "\u041e\u0442\u043e\u043b\u0430\u0440\u0438\u043d\u0433\u043e\u043b\u043e\u0433", "\u041e\u043d\u043a\u043e\u043b\u043e\u0433"
        ])
        self.combo_specialty.setStyleSheet("font-size: 16px;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("\u0412\u0432\u0435\u0434\u0456\u0442\u044c \u043f\u0440\u0456\u0437\u0432\u0438\u0449\u0435 \u0430\u0431\u043e \u0441\u043f\u0435\u0446\u0456\u0430\u043b\u044c\u043d\u0456\u0441\u0442\u044c")
        self.search_input.setStyleSheet("font-size: 16px; padding: 6px;")

        search_button = QPushButton("\u0417\u043d\u0430\u0439\u0442\u0438")
        search_button.setStyleSheet("font-size: 16px; padding: 6px 20px;")
        search_button.clicked.connect(self.load_doctors_from_db)

        search_layout.addWidget(back_button)
        search_layout.addWidget(self.combo_specialty)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        banner = QLabel("\ud83d\udc68\u200d\u2695\ufe0f <b>\u041b\u0406\u041a\u0410\u0420</b> \u2014 \u041c\u0438 \u0437\u043d\u0430\u0439\u0434\u0435\u043c\u043e \u0434\u043b\u044f \u0432\u0430\u0441 \u0456\u0434\u0435\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043b\u0456\u043a\u0430\u0440\u044f")
        banner.setStyleSheet("""
            background-color: #e6f9e6;
            padding: 14px;
            border-radius: 12px;
            font-size: 20px;
        """)

        self.doctor_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background: transparent")
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.doctor_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        main_layout.addLayout(search_layout)
        main_layout.addWidget(banner)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.load_doctors_from_db()

    def load_doctors_from_db(self):
        while self.doctor_layout.count():
            child = self.doctor_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        cursor = self.db.cursor()

        specialty_filter = self.combo_specialty.currentText()
        search_text = self.search_input.text().strip().lower()

        query = '''
            SELECT
                ui.full_name,
                d.specialization,
                d.hospital
            FROM doctors d
            JOIN user_info ui ON d.user_id = ui.user_id
        '''

        filters = []
        params = []

        if specialty_filter != "\u0423\u0441\u0456 \u0441\u043f\u0435\u0446\u0456\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u0456":
            filters.append("d.specialization = ?")
            params.append(specialty_filter)

        if search_text:
            filters.append("LOWER(ui.full_name) LIKE ?")
            params.append(f"%{search_text}%")

        if filters:
            query += " WHERE " + " AND ".join(filters)

        cursor.execute(query, params)
        doctors = cursor.fetchall()

        if not doctors:
            not_found = QLabel("\u041b\u0456\u043a\u0430\u0440\u0456\u0432 \u043d\u0435 \u0437\u043d\u0430\u0439\u0434\u0435\u043d\u043e.")
            not_found.setStyleSheet("font-size: 18px; color: white;")
            self.doctor_layout.addWidget(not_found)
            return

        for doc in doctors:
            name, specialty, hospital = doc
            photo_path = "default_doctor.png"
            card = DoctorCard(name, specialty, hospital, photo_path, parent=self)
            self.doctor_layout.addWidget(card)

    def book_appointment(self, doctor_name):
        self.appointment_window = AppointmentWidget(doctor_name, self.user_id)
        self.appointment_window.show()

    def go_back_to_main(self):
        from main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()