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
            background-color: #021a43; 
            border-radius: 20px;
            font-family: 'Inter';
        """)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = Sidebar(self)
        sidebar.open_reminders_requested.connect(self.open_reminders)

        # Передаємо user_id у ContentArea
        content_area = ContentArea(self.user_id)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area)

    def open_reminders(self):
        from reminder_ui import ReminderWindow
        print(f"Відкриваємо нагадування для user_id={self.user_id}")  # Переконайся, що тут є user_id
        self.reminder_window = ReminderWindow(self.user_id)  # Передаємо user_id
        self.reminder_window.show()
