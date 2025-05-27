from PyQt6.QtWidgets import QWidget, QHBoxLayout
from sidebar import Sidebar
from content_area import ContentArea

class EnterWindow(QWidget):
    def __init__(self, user_id=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setWindowTitle("VitalCore - Панель здоров'я")
        self.showFullScreen()
        self.setStyleSheet("""
            background-color: #f5f9ff; 
            font-family: 'Segoe UI';
        """)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = Sidebar(self)
        sidebar.open_reminders_requested.connect(self.open_reminders)

        content_area = ContentArea(self.user_id)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area)

    def open_reminders(self):
        from reminder_ui import ReminderWindow
        print(f"Відкриваємо нагадування для user_id={self.user_id}")
        self.reminder_window = ReminderWindow(self.user_id)
        self.reminder_window.show()

    def open_doctor_search(self):
      from search_ui import DoctorSearchTab
      import sqlite3
      db = sqlite3.connect('medical_program.db')
      self.search_window = DoctorSearchTab(db, self.user_id)
      self.search_window.show()