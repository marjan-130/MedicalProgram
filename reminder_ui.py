import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMessageBox, QScrollArea, QFrame
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QLinearGradient, QColor, QFont
from PyQt6.QtCore import Qt


class ReminderCard(QFrame):
    def __init__(self, icon_path: str, title: str, details: list[str], button_text: str, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("background-color: white; border-radius: 16px;")
        self.setMinimumHeight(160)

        icon_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(64, 64)

        text_layout = QVBoxLayout()
        title_label = QLabel(f"<b>{title}</b>")
        title_label.setFont(QFont("Segoe UI", 16))
        title_label.setStyleSheet("color: #023047;")
        text_layout.addWidget(title_label)
        for line in details:
            lbl = QLabel(line)
            lbl.setFont(QFont("Segoe UI", 13))
            lbl.setStyleSheet("color: #03045e;")
            text_layout.addWidget(lbl)
        text_layout.addStretch()

        # Кнопка
        button = QPushButton(button_text)
        button.setFixedSize(120, 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #a2d2ff;
                color: black;
            }
        """)
        button.clicked.connect(lambda: QMessageBox.information(self, "Дія", f"Виконано: {button_text}"))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(24)
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(button)


class ReminderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мої нагадування")
        self.resize(700, 800)

        # Градієнтний фон
        palette = QPalette()
        grad = QLinearGradient(0, 0, 0, 1)
        grad.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)
        grad.setColorAt(0.0, QColor("#a2d2ff"))
        grad.setColorAt(1.0, QColor("#d0f4ff"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(grad))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(24)

        header = QLabel("МОЇ НАГАДУВАННЯ")
        header.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #03045e;")
        main_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidgetResizable(True)
        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setSpacing(20)

        vbox.addWidget(ReminderCard(
            icon_path="pictures/doctor_icon.png",
            title="Прийом до лікаря",
            details=[
                "Лікар: Д-р Іван Петренко (Кардіолог)",
                "Дата: 28 травня 2025",
                "Час: 15:30"
            ],
            button_text="Записатись"
        ))

        vbox.addWidget(ReminderCard(
            icon_path="pictures/pill_icon.png",
            title="Прийом ліків",
            details=[
                "Ліки: Амоксицилін",
                "Дозування: 500 мг",
                "Час: 09:00, 21:00"
            ],
            button_text="Прийняти"
        ))

        vbox.addWidget(ReminderCard(
            icon_path="pictures/test_tube_icon.png",
            title="Готові результати аналізів",
            details=[
                "Назва: Загальний аналіз крові",
                "Статус: Готово"
            ],
            button_text="Забрати"
        ))

        vbox.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)