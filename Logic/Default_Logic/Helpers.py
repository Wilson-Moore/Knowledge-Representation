import pandas as pd
from Knowledge.Hierarchy import Patient, Symptom, RiskLevel
from Logic.Default_Logic.Engine import DefaultRule, ReiterDefaultEngine


def safe_int(value):
    try:
        return int(float(value))
    except:
        return 0


def create_patient_from_csv_row(row):
    symptoms = []

    symptom_map = {
        "Air Pollution": "air_pollution_exposure",
        "Chest Pain": "chest_pain",
        "Coughing of Blood": "coughing_of_blood",
        "Fatigue": "fatigue",
        "Weight Loss": "weight_loss",
        "Shortness of Breath": "shortness_of_breath"
    }

    for csv_name, internal_name in symptom_map.items():
        if csv_name in row:
            severity = safe_int(row[csv_name])
            symptoms.append(Symptom(internal_name, severity))

    smoking = safe_int(row.get("Smoking", 0))
    if smoking > 0:
        symptoms.append(Symptom("smoking_history", smoking))

    return Patient(
        id=str(row.get("Patient Id", "Unknown")),
        age=safe_int(row.get("Age", 0)),
        gender="M" if str(row.get("Gender", "1")).lower() in ["1", "m", "male"] else "F",
        symptoms=symptoms
    )


def get_lung_cancer_default_rules():
    return [
        DefaultRule("DR1", "heavy_smoker", "HighRisk", RiskLevel.HIGH),
        DefaultRule("DR2", "severe_symptom", "HighRisk", RiskLevel.HIGH),
        DefaultRule("DR3", "is_senior", "MediumRisk", RiskLevel.MEDIUM),
        DefaultRule("DR4", "high_pollution", "MediumRisk", RiskLevel.MEDIUM),
        DefaultRule("DR5", "chest_pain", "MediumRisk", RiskLevel.MEDIUM),
    ]


def analyze_with_default_logic(df):
    engine = ReiterDefaultEngine(get_lung_cancer_default_rules())
    results = []

    for _, row in df.iterrows():
        patient = create_patient_from_csv_row(row)
        evaluation = engine.evaluate(patient)

        actual = str(row.get("Level", "Low")).capitalize()
        actual_risk = RiskLevel(actual) if actual in ["Low", "Medium", "High"] else None

        results.append({
            "patient_id": patient.id,
            "predicted": evaluation["predicted"],
            "actual": actual_risk,
            "correct": evaluation["predicted"] == actual_risk,
            "applied_rules": evaluation["applied_rules"]
        })

    return results
