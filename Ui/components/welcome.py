from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import os
from .navbar import Navbar
from ..Helpers.Image_radius import ImageRadius
from ..Helpers.responsive import ResponsiveMixin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "..", "assets", "lung-cancer.webp")

class WelcomePage(QWidget, ResponsiveMixin):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.navbar = Navbar(self.stack)
        # content image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image = QPixmap(image_path)

        if self.image.isNull():
            print("Failed to load image")
        else:
            self.image_label.setPixmap(ImageRadius.rounded_pixmap(self.image, radius=50))

        self.subtitle = QLabel(
            "This tool assists in evaluating disease risk\n"
            "based on patient information and symptoms"
        )
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("""
            font-size: 18px;
            color: #34495e;
        """)

        # info page Button
        self.start_btn = QPushButton("Start Diagnosis")
        self.start_btn.setFixedWidth(180)
        self.start_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 8px;
                background-color: #3498db;
                color: white;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        # Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.navbar)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.subtitle)
        main_layout.addSpacing(25)
        main_layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        self.setLayout(main_layout)