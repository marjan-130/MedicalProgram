from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QScrollArea, QSizePolicy, QSpacerItem)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize
import os

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
        
        # Головний контейнер для контенту
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(25)
        
        # Встановлюємо заголовок
        self._setup_header()
        
        # Додаємо секцію найближчого візиту
        self._setup_upcoming_visit()
        
        # Додаємо секцію календаря (заголовок)
        self._setup_calendar_section()
        
        # Встановлюємо віджет для прокрутки
        self.setWidget(self.content_widget)
    
    def _setup_header(self):
        # Заголовок "Панель здоров'я"
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
        # Створюємо контейнер для візитів
        visits_container = QFrame()
        visits_container.setStyleSheet("""
            background-color: #0a285c;
            border-radius: 15px;
        """)
        visits_layout = QVBoxLayout(visits_container)
        visits_layout.setContentsMargins(25, 20, 25, 20)
        visits_layout.setSpacing(15)
        
        # Верхня частина з заголовком і кнопкою "Всі візити"
        header_layout = QHBoxLayout()
        
        # Заголовок "Найближчий візит"
        visit_title = QLabel("Найближчий візит")
        visit_title.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 700;
            color: white;
            font-size: 20px;
        """)
        
        # Кнопка "Всі візити"
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
        
        # Карточка візиту
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
        
        # Створюємо віджет для аватара
        avatar = QLabel()
        avatar.setFixedSize(50, 50)
        avatar.setStyleSheet("""
            background-color: #0a285c;
            border-radius: 25px;
        """)
        
        # Додаємо іконку аватара, якщо існує
        avatar_path = "img/user.svg"
        if os.path.exists(avatar_path):
            avatar.setPixmap(QIcon(avatar_path).pixmap(QSize(30, 30)))
        
        # Інформація про лікаря
        doctor_info = QVBoxLayout()
        doctor_info.setSpacing(5)
        
        # Секція "ПІБ"
        pib_label = QLabel("ПІБ")
        pib_label.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 600;
            color: #8a94a6;
            font-size: 12px;
        """)
        
        doctor_name = QLabel("Др. Катерина Мельник")
        doctor_name.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 700;
            color: white;
            font-size: 16px;
        """)
        
        doctor_info.addWidget(pib_label)
        doctor_info.addWidget(doctor_name)
        
        # Секція "Спеціалізація"
        spec_layout = QVBoxLayout()
        spec_layout.setSpacing(5)
        
        spec_label = QLabel("Спеціалізація")
        spec_label.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 600;
            color: #8a94a6;
            font-size: 12px;
        """)
        
        spec_value = QLabel("Кардіолог")
        spec_value.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 700;
            color: white;
            font-size: 14px;
        """)
        
        spec_layout.addWidget(spec_label)
        spec_layout.addWidget(spec_value)
        
        # Секція "Дата"
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
        
        date_value = QLabel("Сьогодні, 14:30")
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
        
        # Додаємо всі елементи до карточки візиту
        visit_card_layout.addWidget(avatar)
        visit_card_layout.addLayout(doctor_info, 1)
        visit_card_layout.addLayout(spec_layout, 1)
        visit_card_layout.addLayout(date_layout, 1)
        
        visits_layout.addWidget(visit_card)
        self.content_layout.addWidget(visits_container)
    
    def _setup_calendar_section(self):
        # Створюємо контейнер для календаря
        calendar_container = QFrame()
        calendar_container.setStyleSheet("""
            background-color: #0a285c;
            border-radius: 15px;
        """)
        calendar_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        calendar_layout = QVBoxLayout(calendar_container)
        calendar_layout.setContentsMargins(25, 20, 25, 20)
        
        # Заголовок календаря
        calendar_header = QHBoxLayout()
        
        calendar_title = QLabel("Календар")
        calendar_title.setStyleSheet("""
            font-family: 'Inter';
            font-weight: 700;
            color: white;
            font-size: 20px;
        """)
        
        # Іконка календаря
        calendar_icon = QLabel()
        calendar_icon.setFixedSize(24, 24)
        calendar_icon_path = "img/calendar.svg"
        if os.path.exists(calendar_icon_path):
            calendar_icon.setPixmap(QIcon(calendar_icon_path).pixmap(QSize(24, 24)))
        
        calendar_header.addWidget(calendar_title)
        calendar_header.addWidget(calendar_icon)
        calendar_header.addStretch()
        
        calendar_layout.addLayout(calendar_header)
        
        # Тут буде календар (заповнювач висоти)
        calendar_placeholder = QFrame()
        calendar_placeholder.setMinimumHeight(400)
        calendar_layout.addWidget(calendar_placeholder)
        
        self.content_layout.addWidget(calendar_container)
class NavigationButton(QPushButton):
    def __init__(self, icon_path, text, is_selected=False):
        super().__init__()
        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Установка стилів в залежності від стану
        if is_selected:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #0a285c;
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 15px;
                    color: white;
                    font-weight: 600;
                    font-size: 16px;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 15px;
                    color: #8a94a6;
                    font-weight: 500;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: rgba(10, 40, 92, 0.3);
                }
            """)
        
        # Створюємо горизонтальний лейаут для іконки і тексту
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)
        
        # Додаємо іконку, якщо шлях існує
        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))
        
        # Встановлюємо текст
        self.setText(text)
        
        # Додаємо відступ справа
        self.layout.addStretch()
class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: #051e4a;")
        
        # Головний лейаут для бічної панелі
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 20)
        self.layout.setSpacing(0)
        
        # Додаємо логотип та заголовок
        self._setup_header()
        
        # Додаємо навігаційне меню
        self._setup_navigation()
        
        # Додаємо розтяжку щоб відсунути кнопку виходу вниз
        self.layout.addStretch()
        
        # Додаємо кнопку виходу
        self._setup_exit_button()
    
    def _setup_header(self):
        header = QWidget()
        header.setFixedHeight(100)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 35, 30, 0)
        
        # Логотип (круглий фрейм)
        logo = QPushButton()
        logo.setFixedSize(40, 40)
        logo.setStyleSheet("""
            background-color: #f4f4f4;
            border-radius: 12px;
        """)
        
        # Якщо є SVG логотип, можна встановити його
        logo_path = "img/image.svg"
        if os.path.exists(logo_path):
            logo.setIcon(QIcon(logo_path))
            logo.setIconSize(QSize(24, 24))
        
        # Назва додатку
        title = QLabel("VitalCore")
        title.setStyleSheet("""
            font-weight: 700;
            color: #f4f4f4;
            font-size: 27px;
            margin-left: 15px;
        """)
        
        header_layout.addWidget(logo)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.layout.addWidget(header)
    
    def _setup_navigation(self):
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(20, 40, 20, 0)
        nav_layout.setSpacing(10)
        
        # Пункти навігації з шляхами до іконок
        nav_items = [
            {"icon": "img/SVG.svg", "text": "Головна", "selected": True},
            {"icon": "img/user.svg", "text": "Мій профіль", "selected": False},
            {"icon": "img/bell.svg", "text": "Нагадування", "selected": False},
        ]
        
        for item in nav_items:
            nav_button = NavigationButton(
                item["icon"], 
                item["text"], 
                item["selected"]
            )
            nav_layout.addWidget(nav_button)
            
            # Якщо потрібно додати обробник подій:
            # nav_button.clicked.connect(lambda checked, text=item["text"]: self.on_nav_clicked(text))
        
        self.layout.addWidget(nav_container)
    
    def _setup_exit_button(self):
        exit_button = NavigationButton("img/sign-out-squre-light.svg", "Вийти")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 12px;
                text-align: left;
                padding-left: 15px;
                color: #8a94a6;
                font-weight: 500;
                font-size: 16px;
                margin-left: 20px;
                margin-right: 20px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: rgba(10, 40, 92, 0.3);
            }
        """)
        
        self.layout.addWidget(exit_button)
    
    def on_nav_clicked(self, text):
        # Обробник кліку по пункту навігації
        print(f"Clicked on: {text}")
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
        # Головний лейаут
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Додаємо бічну панель
        sidebar = Sidebar(self)
        main_layout.addWidget(sidebar)
        
        # Додаємо основний контент
        content_area = ContentArea(self)
        main_layout.addWidget(content_area)
