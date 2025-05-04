from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QPixmap, QFontDatabase, QFont, QPainter
from PyQt6.QtCore import Qt
from login_ui import LoginWindow
from Alogoritm import handle_button_click, on_db_connection_result, DbConnectionThread

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VitalCore")
        self.showFullScreen()
        self.background_path = "pictures/backgroundMain.png"
        self.init_ui()

    def init_ui(self):
        wendy_font, marck_font = self.load_fonts()

        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        center_frame = self.create_center_frame()

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.setSpacing(25)

        title = QLabel("VitalCore")
        title.setFont(QFont(wendy_font, 32))
        title.setStyleSheet("color: #0077CC;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.create_buttons(vbox, marck_font)

        vbox.insertWidget(0, title)
        center_frame.setLayout(vbox)

        main_layout.addWidget(center_frame)
        self.setLayout(main_layout)

    def load_fonts(self):
        wendy_id = QFontDatabase.addApplicationFont("fonts/WendyOne-Regular.ttf")
        marck_id = QFontDatabase.addApplicationFont("fonts/MarckScript-Regular.ttf")
        wendy_font = QFontDatabase.applicationFontFamilies(wendy_id)[0]
        marck_font = QFontDatabase.applicationFontFamilies(marck_id)[0]

        return wendy_font, marck_font

    def create_center_frame(self):
        center_frame = QFrame()
        center_frame.setFixedSize(420, 500)
        center_frame.setStyleSheet("""
            QFrame {
                background-color: #D1FBFF;
                border-radius: 30px;
                border: none;
            }
        """)
        return center_frame

    def create_buttons(self, vbox, marck_font):
        for text in ["Enter", "Login", "Exit"]:
            btn = QPushButton(text)
            btn.setFixedSize(220, 45)
            btn.setFont(QFont(marck_font, 16))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #66BFFF;
                    color: white;
                    font-style: italic;
                    border-radius: 20px;
                }
                QPushButton:hover {
                    background-color: #55AAEE;
                }
            """)
            btn.clicked.connect(lambda _, t=text: self.handle_button_click(t))
            vbox.addWidget(btn)

    def handle_button_click(self, text: str):
        if text == "Enter":
            QMessageBox.information(self, "Info", "Enter pressed (without DB connection).")
        elif text == "Exit":
            QApplication.quit()
        elif text == "Login":
            self.login_window = LoginWindow(self.login_success)
            self.login_window.show()

    def login_success(self, username):
        print(f"[INFO] User '{username}' successfully logged in.")
        QMessageBox.information(self, "Login", f"Welcome, {username}!")
        # TODO: You can transition to another window here or display user profile data.
    
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.background_path).scaled(
            self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        painter.drawPixmap(self.rect(), pixmap)

    def start_db_connection_thread(self):
        print("Starting DB connection thread...")
        self.db_thread = DbConnectionThread()
        self.db_thread.result.connect(lambda connection: on_db_connection_result(connection, self))
        self.db_thread.start()
