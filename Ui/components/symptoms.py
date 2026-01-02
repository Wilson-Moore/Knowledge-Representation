from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox,
    QPushButton, QVBoxLayout,
    QSizePolicy, QSlider
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
        patient_data["symptoms"] = {}

        self.symptom_sliders = {}

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

        self.symptoms_model.itemChanged.connect(self.on_sym_change)
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

        # Slider For Selecting the severity
        self.sliders_layout = QVBoxLayout()
        self.sliders_layout.setSpacing(10)

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
        self.main_layout = QVBoxLayout()
        wrapper = QWidget()
        self.container = QHBoxLayout()
        wrapper.setLayout(self.container)
        left_col = QVBoxLayout()
        left_col.addWidget(self.image_label)
        left_col.addStretch()
        right_col = QVBoxLayout()
        right_col.addLayout(select_row)
        right_col.addLayout(self.sliders_layout) 
        right_col.addWidget(self.next_btn, alignment=Qt.AlignCenter)
        right_col.addStretch() 

        self.container.addLayout(left_col, stretch=1)
        self.container.addLayout(right_col, stretch=0)
        self.container.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.main_layout.addWidget(self.navbar)
        self.main_layout.addWidget(wrapper)

        self.setLayout(self.main_layout)


    def next_page(self):
        if not self.next_btn.isEnabled():
            return
        patient_data["method"] = self.method_dropdown.currentText()
        self.stack.setCurrentIndex(3)

    def on_sym_change(self, item):
        symptom = item.text()

        if item.checkState() == Qt.Checked:
            self.show_range(symptom, 1, 10)
        else:
            self.remove_range(symptom)
            print(f"Uncheked {item.text()}")

    def show_range(self, symptom, min, max):
        if symptom in self.symptom_sliders:
            return
        label = QLabel(symptom)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setValue(1)
        slider.setObjectName(symptom)

        slider.valueChanged.connect(
            lambda val, s=symptom: self.on_slid_change(s, val)
        )
        self.symptom_sliders[symptom] = (label, slider)
        self.sliders_layout.addWidget(label)
        self.sliders_layout.addWidget(slider)
        patient_data["symptoms"][symptom] = {
            "key": SYMPTOMS[symptom],
            "severity": 1
        }
    def remove_range(self, symptom):
        if symptom not in self.symptom_sliders:
            return

        label, slider = self.symptom_sliders.pop(symptom)

        label.deleteLater()
        slider.deleteLater()
        patient_data["symptoms"].pop(symptom)

        patient_data.setdefault("symptoms_severity", {})
        patient_data["symptoms_severity"].pop(symptom, None)

    def on_slid_change(self, symptom, value):
        patient_data["symptoms"][symptom]["severity"] = value
