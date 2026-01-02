from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QMovie, QFont, QPalette, QColor
import os
import pandas as pd
import random
from pprint import pprint

from .navbar import Navbar
from ..Helpers.responsive import ResponsiveMixin

from ..state.shared import patient_data

from Logic.Modal_Logic.Helpers import analyze_dataset_with_kripke
from Logic.Fuzzy_logic.Helpers import analyze_dataset_with_fuzzy
from Logic.Default_Logic.Helpers import analyze_with_default_logic
from Logic.Belief_Functions.Helpers import analyze_with_belief

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
spinner_path = os.path.join(BASE_DIR, "..", "assets", "spinner.gif")

ANALYSIS_MAP = {
    "Modal reasoning": analyze_dataset_with_kripke,
    "Default reasoning": analyze_with_default_logic,
    "Fuzzy reasoning": analyze_dataset_with_fuzzy,
    "Belief": analyze_with_belief
}
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
    'Snoring': 'snoring'
}
class ResultPage(QWidget, ResponsiveMixin):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.navbar = Navbar(self.stack)

        # Title
        self.title = QLabel("Diagnosis Result")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        # Spinner
        self.spinner_label = QLabel()
        self.spinner_label.setAlignment(Qt.AlignCenter)

        self.spinner = QMovie(spinner_path)
        self.spinner_label.setFixedSize(320, 320)
        self.spinner.setScaledSize(QSize(320, 320))
        self.spinner_label.setMovie(self.spinner)
        self.spinner.start()
        # Loading Text
        self.loading_text = QLabel("Analyzing patient data...")
        self.loading_text.setAlignment(Qt.AlignCenter)
        self.loading_text.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        # Result
        self.result_card = QWidget()
        self.result_card.setVisible(False)
        self.result_card.setStyleSheet("""
            QWidget {
                background-color: #f9fafb;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
            }
        """)
        self.result_label = QLabel()
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignLeft)
        self.result_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: #2c3e50;
                line-height: 1.6;
                padding: 25px;
            }
        """)
        card_layout = QVBoxLayout(self.result_card)
        card_layout.setContentsMargins(30, 25, 30, 25)
        card_layout.addWidget(self.result_label)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.navbar)
        main_layout.addWidget(self.title)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.spinner_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.loading_text, alignment=Qt.AlignCenter)
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.result_card)
        center_layout.addStretch()
        main_layout.addLayout(center_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.result_card.hide()
        self.spinner_label.show()
        self.loading_text.show()
        self.spinner.start()

        # prediction delay
        QTimer.singleShot(2000, self.show_results)

    def show_results(self):
        self.spinner.stop()
        self.spinner_label.hide()
        self.loading_text.hide()

        df = self.build_dataframe_from_patient()
        method = (patient_data.get("method") or "").strip()
        analyze_fn = ANALYSIS_MAP.get(method)
       
        if not analyze_fn:
            self.result_label.setText("No reasoning method selected")
            self.result_label.setVisible(True)
            return
        if method == "Belief" or method == "Fuzzy reasoning":
            results = analyze_fn(df, True)
        else:
            results = analyze_fn(df)
        if not results:
            self.result_label.setText("Unable to analyze patient data.")
            self.result_label.setVisible(True)
            return

        result = results[0]

        predicted = result.get('predicted_risk') or result.get('predicted')
        # actual = result.get('actual_risk')
        # top_predictions = result['top_predictions']
        selected_symptoms = patient_data.get("symptoms", [])

        if selected_symptoms:
            symptoms_html = "<ul style='margin-left:15px;'>"
            for s in selected_symptoms:
                symptoms_html += f"<li>{s}</li>"
            symptoms_html += "</ul>"
        else:
            symptoms_html = "<i>No symptoms reported</i>"

        risk_color = {
            "Low": "#27ae60",
            "Medium": "#f39c12",
            "High": "#e74c3c"
        }.get(predicted.value if predicted else "", "#34495e")

        text = f"""
        <div style="max-width:520px;">

        <h1 style="font-size:22px; margin-bottom:12px;">
            Patient Summary
        </h1>

        <p style="font-size:16px;">
        <b>Age:</b> {patient_data.get("age")} Years Old<br>
        <b>Gender:</b> {patient_data.get("gender")}<br>
        <b>Reasoning Method:</b> {method}
        </p>

        <hr style="margin:18px 0;">

        <h2 style="font-size:18px;">Symptoms Detected</h2>
        <p style="font-size:16px;">
        {symptoms_html}
        </p>

        <hr style="margin:18px 0;">

        <h2 style="font-size:18px;">Diagnosis Result</h2>

        <div style="
            margin-top:10px;
            font-size:22px;
            font-weight:bold;
            color:{risk_color};
        ">
            {predicted.value if predicted else 'Unknown'}
        </div>

        </div>
        """

        self.result_label.setText(text)
        self.result_card.setVisible(True)

    def build_dataframe_from_patient(self):
        patient_dict = {
            "Patient Id": random.randint(1000, 9999),
            "Age": int(patient_data["age"]) if patient_data.get("age") is not None else random.randint(20, 70),
            "Gender": 1 if patient_data.get("gender", "M") in ["M", "Male"] else 0,
            "Air Pollution": 0,
            "Alcohol use": 0,
            "Dust Allergy": 0,
            "OccuPational Hazards": 0,
            "Chest Pain": 0,
            "Coughing of Blood": 0,
            "Fatigue": 0,
            "Weight Loss": 0,
            "Shortness of Breath": 0,
            "Wheezing": 0,
            "Swallowing Difficulty": 0,
            "Frequent Cold": 0,
            "Dry Cough": 0,
            "Snoring": 0,
            "Smoking": 0,
            "Passive Smoker": 0,
            "Level": "LOW"
        }

        for symptom, data in patient_data.get("symptoms", {}).items():
            severity = data.get("severity", 1)
            patient_dict[symptom] = severity
        return pd.DataFrame([patient_dict])
