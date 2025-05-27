from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QIcon, QPalette, QBrush, QLinearGradient, QColor
from PyQt6.QtCore import Qt, QSize, pyqtSignal
import os
import session
from profile_ui import ProfileWindow

class NavigationButton(QPushButton):
    def __init__(self, icon_path, text, is_selected=False):
        super().__init__()
        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if is_selected:
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 15px;
                    color: #023047;
                    font-weight: 600;
                    font-size: 16px;
                    font-family: 'Inter';
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 15px;
                    color: #023047;
                    font-weight: 500;
                    font-size: 16px;
                    font-family: 'Inter';
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                    color: #023047;
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
    open_reminders_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        self.setStyleSheet("background: transparent;")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 20)
        self.layout.setSpacing(0)

        self._setup_header()
        self._setup_navigation()
        self.layout.addStretch()
        self._setup_exit_button()

    def resizeEvent(self, event):
        # Оновлюємо градієнт при зміні розміру
        self.update_gradient()
        super().resizeEvent(event)

    def update_gradient(self):
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#a2d2ff"))  # Темно-синій
        gradient.setColorAt(1.0, QColor("#d0f4ff"))  # Бірюзовий
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def _setup_header(self):
        header = QWidget()
        header.setFixedHeight(100)
        header.setStyleSheet("background: transparent;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 35, 30, 0)

        logo = QPushButton()
        logo.setFixedSize(40, 40)
        logo.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 12px;
        """)

        logo_path = "img/image.svg"
        if os.path.exists(logo_path):
            logo.setIcon(QIcon(logo_path))
            logo.setIconSize(QSize(24, 24))

        title = QLabel("VitalCore")
        title.setStyleSheet("""
            font-weight: 700;
            color: white;
            font-size: 27px;
            margin-left: 15px;
            font-family: 'Inter';
        """)

        header_layout.addWidget(logo)
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.layout.addWidget(header)

    def _setup_navigation(self):
        nav_container = QWidget()
        nav_container.setStyleSheet("background: transparent;")
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(20, 40, 20, 0)
        nav_layout.setSpacing(10)

        nav_items = [
            {"icon": "img/SVG.svg", "text": "Головна", "selected": True},
            {"icon": "img/user.svg", "text": "Мій профіль", "selected": False},
            {"icon": "img/bell.svg", "text": "Нагадування", "selected": False},
            {"icon": "img/search.svg", "text": "Пошук лікарів", "selected": False}
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
            print("Користувач не авторизований, перехід у профіль заборонено.")
        elif text == "Головна":
          self.return_to_main_menu()
        elif text == "Нагадування":
          self.open_reminders_requested.emit()
        elif text == "Пошук лікарів":  # Додано новий обробник
          self.open_doctor_search()
        else:
          print(f"Clicked on: {text}")

    def open_doctor_search(self):
        from search_ui import DoctorSearchTab
        import sqlite3
        db = sqlite3.connect('medical_program.db')  # Зверніть увагу на правильну назву бази
        user_id = session.get_session_user_id()
        self.search_window = DoctorSearchTab(db, user_id)
        self.search_window.show()

    def open_profile(self, user_id):
        parent_widget = self.window()
        parent_widget.close()
        self.profile_window = ProfileWindow(user_id)
        self.profile_window.show()
