from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox,
    QPushButton, QVBoxLayout,
    QSizePolicy
)
from PyQt5.QtWidgets import QHBoxLayout, QListView, QAbstractItemView
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import os

from .navbar import Navbar
from ..Helpers.Image_radius import ImageRadius
from ..Helpers.responsive import ResponsiveMixin
from ..Helpers.select_box import MultiSelectComboBox
from ..Helpers.funcs import Funcs

from ..state.shared import patient_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "..", "assets", "lung-cancer.webp")

SYMPTOMS = {
    'Air Pollution': 'air_pollution_exposure',
    'Alcohol use': 'alcohol_use',
    'Dust Allergy': 'dust_allergy',
    'OccuPational Hazards': 'occupational_exposure',
    'Chest Pain': 'chest_pain',
    'Coughing of Blood': 'coughing_blood',
    'Fatigue': 'fatigue',
    'Weight Loss': 'weight_loss',
    'Shortness of Breath': 'shortness_of_breath',
    'Wheezing': 'wheezing',
    'Swallowing Difficulty': 'swallowing_difficulty',
    'Frequent Cold': 'frequent_cold',
    'Dry Cough': 'dry_cough',
    'Snoring': 'snoring',
    'Smoking': 'smoking'
}

class SymptomsPage(QWidget, ResponsiveMixin):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.checkboxes = {}
        self.funcs = Funcs(patient_data)

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

        self.symptoms_dropdown = MultiSelectComboBox()
        view = QListView()
        view.setSelectionMode(QAbstractItemView.NoSelection)
        self.symptoms_dropdown.setView(view)
        self.symptoms_dropdown.setFixedWidth(220)
        self.symptoms_dropdown.setEditable(True)
        self.symptoms_dropdown.lineEdit().setReadOnly(True)
        self.symptoms_dropdown.lineEdit().setPlaceholderText("Select symptoms")
        self.symptoms_dropdown.setMinimumHeight(40)
        
        self.symptoms_model = QStandardItemModel()
        for symptom in SYMPTOMS.keys():
            item = QStandardItem(symptom)
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.symptoms_model.appendRow(item)

        self.symptoms_dropdown.setModel(self.symptoms_model)
        self.symptoms_dropdown.view().pressed.connect(
            lambda index: self.funcs.toggle_item(index, self.symptoms_model)
        )
        self.symptoms_model.itemChanged.connect(
            lambda: self.funcs.update_selected_symptoms(
                self.symptoms_dropdown,
                self.symptoms_model,
                self.method_dropdown,
                self.next_btn
            )
        )

        # Method selecting (Modal, Default, Fuzzy)
        self.method_dropdown = QComboBox()
        self.method_dropdown.addItems([
            "Select method",
            "Modal reasoning",
            "Default reasoning",
            "Fuzzy reasoning",
            "Belief"
        ])
        self.method_dropdown.setFixedWidth(220)
        self.method_dropdown.setStyleSheet(f"""
                padding: 8px;
        """)
        
        select_row = QHBoxLayout()
        select_row.addWidget(self.symptoms_dropdown, stretch=3)
        select_row.addSpacing(15)
        select_row.addWidget(self.method_dropdown, stretch=1)
        self.symptoms_dropdown.setMinimumHeight(40)
        self.method_dropdown.currentIndexChanged.connect(
            lambda: self.funcs.validate_form(
                self.symptoms_model,
                self.method_dropdown,
                self.next_btn
            )
        )

        # Button Takes To results
        self.next_btn = QPushButton("Start Diagnosis")
        self.next_btn.setFixedWidth(180)
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
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.clicked.connect(self.next_page)

        # Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.navbar)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(select_row)
        main_layout.addWidget(self.next_btn, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def next_page(self):
        if not self.next_btn.isEnabled():
            return
        patient_data["symptoms"] = self.funcs.get_selected_symptoms(self.symptoms_model)
        patient_data["method"] = self.method_dropdown.currentText()
        self.stack.setCurrentIndex(3)