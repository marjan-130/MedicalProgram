from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
import os

# Імпортуємо функцію для роботи з сесією
import session
from profile_ui import ProfileWindow  # Імпорт вікна профілю

class NavigationButton(QPushButton):
    def __init__(self, icon_path, text, is_selected=False):
        super().__init__()
        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

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

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)

        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))

        self.setText(text)
        self.layout.addStretch()

class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: #051e4a;")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 20)
        self.layout.setSpacing(0)

        self._setup_header()
        self._setup_navigation()
        self.layout.addStretch()
        self._setup_exit_button()

    def _setup_header(self):
        header = QWidget()
        header.setFixedHeight(100)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 35, 30, 0)

        logo = QPushButton()
        logo.setFixedSize(40, 40)
        logo.setStyleSheet("""
            background-color: #f4f4f4;
            border-radius: 12px;
        """)

        logo_path = "img/image.svg"
        if os.path.exists(logo_path):
            logo.setIcon(QIcon(logo_path))
            logo.setIconSize(QSize(24, 24))

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
            nav_button.clicked.connect(lambda checked, text=item["text"]: self.on_nav_clicked(text))
            nav_layout.addWidget(nav_button)

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
        exit_button.clicked.connect(self.return_to_main_menu)
        self.layout.addWidget(exit_button)

    def return_to_main_menu(self):
        from main_window import MainWindow
        parent_widget = self.window()
        parent_widget.close()
        self.main_window = MainWindow()
        self.main_window.show()

    def on_nav_clicked(self, text):
        if text == "Мій профіль":
            user_id = session.get_session_user_id()
            if user_id is not None:
                self.open_profile(user_id)
            else:
                # Якщо сесія відсутня - можна вивести повідомлення або нічого не робити
                print("Користувач не авторизований, перехід у профіль заборонено.")
        elif text == "Головна":
            self.return_to_main_menu()
        else:
            print(f"Clicked on: {text}")

    def open_profile(self, user_id):
        parent_widget = self.window()
        parent_widget.close()
        self.profile_window = ProfileWindow(user_id)
        self.profile_window.show()
