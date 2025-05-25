import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QScrollArea, QFrame
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QLinearGradient, QColor, QFont
from PyQt6.QtCore import Qt


class ReminderCard(QFrame):
    def init(self, icon_path: str, title: str, details: list[str], button_text: str, parent=None):
        super().init(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("background-color: white; border-radius: 12px;")
        self.setFixedHeight(120)

        # ������
        icon_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(48, 48)

        # �����
        text_layout = QVBoxLayout()
        title_label = QLabel(f"<b>{title}</b>")
        title_label.setFont(QFont("Segoe UI", 14))
        title_label.setStyleSheet("color: #023047;")
        text_layout.addWidget(title_label)
        for line in details:
            lbl = QLabel(line)
            lbl.setFont(QFont("Segoe UI", 12))
            lbl.setStyleSheet("color: #03045e;")
            text_layout.addWidget(lbl)
        text_layout.addStretch()

        # ������
        button = QPushButton(button_text)
        button.setFixedSize(100, 36)
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #a2d2ff;
                color: black;
            }
        """)
        button.clicked.connect(lambda: QMessageBox.information(self, "ĳ�", f"��������: {button_text}"))

        # ������� ������
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.addWidget(icon_label)
        layout.addSpacing(12)
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(button)


class ReminderWindow(QWidget):
    def init(self):
        super().init()
        self.setWindowTitle("�����������")
        self.resize(600, 700)

        # ���䳺����� ���
        palette = QPalette()
        grad = QLinearGradient(0, 0, 0, 1)
        grad.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)
        grad.setColorAt(0.0, QColor("#a2d2ff"))
        grad.setColorAt(1.0, QColor("#d0f4ff"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(grad))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        header = QLabel("�����������")
        header.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #03045e;")
        main_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidgetResizable(True)
        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setSpacing(12)

        # 1) ������ �� �����
        vbox.addWidget(ReminderCard(
            icon_path="pictures/doctor_icon.png",
            title="������ �� �����",
            details=[
                "˳���: �-� ���� �������� (��������)",
                "����: 28 ������ 2025",
                "���: 15:30"
            ],
            button_text="����������"
        ))

        # 2) ������ ���
        vbox.addWidget(ReminderCard(
            icon_path="pictures/pill_icon.png",
            title="������ ���",
            details=[
                "˳��: ����������",
                "���������: 500 ��",
                "���: 09:00, 21:00"
            ],
            button_text="��������"
        ))

# 3) ����� ���������� ������
        vbox.addWidget(ReminderCard(
            icon_path="pictures/test_tube_icon.png",
            title="����� ���������� ������",
            details=[
                "�����: ��������� ����� ����",
                "������: ������"
            ],
            button_text="�������"
        ))

        vbox.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)
