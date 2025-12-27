from PyQt5.QtWidgets import (
    QWidget, QLabel, QSpinBox, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont

import os

from ..Helpers.Image_radius import ImageRadius
from ..Helpers.responsive import ResponsiveMixin
from .navbar import Navbar

from ..state.shared import patient_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "..", "assets", "lung-cancer.webp")

class PatientPage(QWidget, ResponsiveMixin):
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
            
        label_font = QFont("Arial", 16, QFont.Bold)
        # Age
        self.age_label = QLabel("Age")
        self.age_label.setFont(label_font)
        self.age = QSpinBox()
        self.age.setRange(0, 120)
        self.age.setValue(0)
        self.age.setSpecialValueText("Select")
        self.age.setMaximumWidth(100)

        # Gender
        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female"])
        self.gender.setMaximumWidth(120)
        self.gender.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.gender.setStyleSheet("""
            QComboBox {
                font-size: 24px;
                padding: 5px;
                border: 1px solid #3498db;
                border-radius: 6px;
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QComboBox:hover {
                border: 2px solid #2980b9;
            }
            QComboBox:focus {
                border: 2px solid #2980b9;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(path_to_arrow_icon.png);  # optional custom arrow
                width: 10px;
                height: 10px;
            }
        """)
        self.gender.insertItem(0, "Select gender")
        self.gender.setCurrentIndex(0)

        # Layout Gender & Age 
        age_gender_layout = QHBoxLayout()
        age_layout = QVBoxLayout()
        age_layout.addWidget(self.age_label)
        age_layout.addWidget(self.age)

        self.age.valueChanged.connect(self.validate_inputs)

        gender_label = QLabel("Gender")
        gender_layout = QVBoxLayout()
        gender_label.setFont(label_font)
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender)
        self.gender.currentIndexChanged.connect(self.validate_inputs)

        age_gender_layout.addLayout(age_layout)
        age_gender_layout.addSpacing(20)
        age_gender_layout.addLayout(gender_layout)

        # Sytmptoms Page Button
        self.next_btn = QPushButton("Enter Sutmptoms")
        self.next_btn.setFixedWidth(180)
        self.next_btn.setStyleSheet("""
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
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.clicked.connect(self.next_page)
        self.next_btn.setEnabled(False)
        self.next_btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    padding: 8px;
                    background-color: #bdc3c7;
                    color: white;
                    border-radius: 6px;
                }
                QPushButton:enabled {
                    background-color: #3498db;
                }
                QPushButton:enabled:hover {
                    background-color: #2980b9;
                }
            """)

        # Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.navbar)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(age_gender_layout)
        main_layout.addWidget(self.next_btn, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def next_page(self):
        patient_data["age"] = self.age.value()
        patient_data["gender"] = self.gender.currentText()
        self.stack.setCurrentIndex(2)

    def validate_inputs(self):
        age_valid = self.age.value() > 0
        gender_valid = self.gender.currentIndex() != 0
        self.next_btn.setEnabled(age_valid and gender_valid)
