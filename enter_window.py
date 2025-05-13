from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QScrollArea, QCheckBox)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QPainter
from PyQt6.QtCore import Qt, QSize

class EnterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VitalCore - Панель здоров'я")
        self.showFullScreen()
        self.setStyleSheet("""
            background-color: #021a43; 
            border-radius: 20px;
            font-family: 'Inter';
        """)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Бічна панель
        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("background-color: #051e4a;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # Лого та заголовок
        header = QWidget()
        header.setFixedHeight(100)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 35, 30, 0)
        
        icon_btn = QPushButton()
        icon_btn.setFixedSize(40, 40)
        icon_btn.setStyleSheet("""
            background-color: #f4f4f4;
            border-radius: 12px;
        """)
        
        title = QLabel("VitalCore")
        title.setStyleSheet("""
            font-weight: 700;
            color: #f4f4f4;
            font-size: 27px;
            margin-left: 15px;
        """)
        
        header_layout.addWidget(icon_btn)
        header_layout.addWidget(title)
        sidebar_layout.addWidget(header)

        # Навігація (спрощена версія)
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(30, 30, 30, 30)
        
        # Додаткові кнопки навігації можна додати тут...
        
        sidebar_layout.addWidget(nav_widget)
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # Основний вміст
        content_scroll = QScrollArea()
        content_scroll.setWidgetResizable(True)
        content_scroll.setStyleSheet("""
            QScrollArea { border: none; }
            QScrollBar:vertical { width: 0px; }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Заголовок
        title = QLabel("Панель здоров'я")
        title.setStyleSheet("""
            font-weight: 700;
            color: white;
            font-size: 28px;
        """)
        content_layout.addWidget(title)

        # Картки статистики
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        stats_data = [
            ("4", "Готові аналізи"),
            ("+5", "Направлення"),
            ("+5", "Важливі показники")
        ]
        
        for value, text in stats_data:
            card = QFrame()
            card.setFixedSize(176, 161)
            card.setStyleSheet("""
                background-color: #0a285c;
                border-radius: 15px;
                border: 1px solid #051e4a;
            """)
            
            card_layout = QVBoxLayout(card)
            card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            value_label = QLabel(value)
            value_label.setStyleSheet("""
                font-weight: 700;
                color: white;
                font-size: 28px;
            """)
            
            text_label = QLabel(text)
            text_label.setStyleSheet("""
                font-weight: 500;
                color: white;
                font-size: 15px;
            """)
            
            card_layout.addWidget(value_label)
            card_layout.addWidget(text_label)
            stats_layout.addWidget(card)
        
        content_layout.addLayout(stats_layout)

        # Візити та календар
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        
        # Візити
        visits_frame = QFrame()
        visits_frame.setFixedSize(569, 531)
        visits_frame.setStyleSheet("""
            background-color: #0a285c;
            border-radius: 15px;
            border: 1px solid #051e4a;
        """)
        
        visits_layout = QVBoxLayout(visits_frame)
        visits_layout.setContentsMargins(20, 20, 20, 20)
        
        visits_title = QLabel("Найближчі візити")
        visits_title.setStyleSheet("""
            font-weight: 700;
            color: white;
            font-size: 19px;
        """)
        visits_layout.addWidget(visits_title)
        
        # Приклади візитів
        appointments = [
            ("Др. Катерина Мельник", "Керівник", "Сьогодні, 14:30"),
            ("Др. Андрій Петренко", "Тереневт", "24 квітня, 10:15"),
            ("Др. Ірина Коваленко", "Невролог", "30 квітня, 13:00")
        ]
        
        for doctor, specialty, time in appointments:
            visit = QFrame()
            visit.setFixedHeight(80)
            visit.setStyleSheet("""
                background-color: #041e49;
                border-radius: 12px;
            """)
            
            visit_layout = QHBoxLayout(visit)
            visit_layout.setContentsMargins(15, 10, 15, 10)
            
            # Інформація про лікаря
            info_layout = QVBoxLayout()
            doctor_label = QLabel(doctor)
            doctor_label.setStyleSheet("""
                font-weight: 700;
                color: white;
                font-size: 15px;
            """)
            
            specialty_label = QLabel(specialty)
            specialty_label.setStyleSheet("""
                font-weight: 400;
                color: white;
                font-size: 13px;
            """)
            
            info_layout.addWidget(doctor_label)
            info_layout.addWidget(specialty_label)
            
            # Час візиту
            time_label = QLabel(time)
            time_label.setStyleSheet("""
                font-weight: 500;
                color: white;
                font-size: 13px;
            """)
            time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            
            visit_layout.addLayout(info_layout, 70)
            visit_layout.addWidget(time_label, 30)
            
            visits_layout.addWidget(visit)
        
        bottom_layout.addWidget(visits_frame)
        
        # Календар (спрощена версія)
        calendar_frame = QFrame()
        calendar_frame.setFixedSize(500, 583)
        calendar_frame.setStyleSheet("""
            background-color: #0a285c;
            border-radius: 15px;
            border: 1px solid #051e4a;
        """)
        
        calendar_layout = QVBoxLayout(calendar_frame)
        calendar_layout.setContentsMargins(20, 20, 20, 20)
        
        calendar_title = QLabel("January")
        calendar_title.setStyleSheet("""
            font-weight: 700;
            color: white;
            font-size: 19px;
        """)
        calendar_layout.addWidget(calendar_title)
        
        # Тут можна додати повноцінний календар
        
        bottom_layout.addWidget(calendar_frame)
        content_layout.addLayout(bottom_layout)
        
        content_scroll.setWidget(content_widget)
        main_layout.addWidget(content_scroll)