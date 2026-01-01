import pandas as pd
from typing import List, Dict
from .Engine import FuzzyLungDiseaseSystem
from Knowledge.Hierarchy import RiskLevel

from Knowledge.Hierarchy import Patient, Symptom

def create_patient_from_csv_row(row):
    """Crée un objet Patient à partir d'une ligne CSV"""
    patient_id = str(row.get('Patient Id', row.get('index', 'Unknown')))
    age = int(row.get('Age', 50))
    
    # Créer le patient
    patient = Patient(id=patient_id, age=age, gender="unknown", symptoms=[])
    
    # Ajouter seulement les 7 symptômes utilisés par le moteur flou
    # Noms exacts des colonnes CSV
    important_symptoms = [
        ('Smoking', 'Smoking'),
        ('Air Pollution', 'Air Pollution'),
        ('Coughing of Blood', 'Coughing of Blood'),
        ('Chest Pain', 'Chest Pain'),
        ('Shortness of Breath', 'Shortness of Breath'),
        ('Weight Loss', 'Weight Loss')
    ]
    
    for csv_col, symptom_name in important_symptoms:
        if csv_col in row:
            # Les valeurs dans le CSV vont de 1 à 9, on les convertit en échelle 0-10
            csv_value = float(row[csv_col])
            
            # Conversion de l'échelle 1-9 à 0-10
            # Formule: (valeur - 1) * (10 / 8)
            if csv_value >= 1 and csv_value <= 9:
                normalized_value = (csv_value - 1) * (10.0 / 8.0)
            else:
                normalized_value = csv_value  # Garder tel quel si hors plage
                
            symptom = Symptom(name=symptom_name, severity=normalized_value)
            patient.symptoms.append(symptom)
    
    # DEBUG: Afficher les valeurs
    print(f"\n[CREATE PATIENT] {patient_id}")
    print(f"  Age: {age}")
    for symptom in patient.symptoms:
        print(f"  {symptom.name}: {symptom.severity:.2f} (original: {row.get(symptom.name, 'N/A')})")
    
    return patient
def analyze_dataset_with_fuzzy(df: pd.DataFrame, verbose: bool = True) -> List[Dict]:
    """Analyse le dataset avec la logique floue"""
    fuzzy_system = FuzzyLungDiseaseSystem()
    results = []
    
    if verbose:
        print("=" * 70)
        print("LUNG CANCER RISK ASSESSMENT - SIMPLIFIED FUZZY LOGIC")
        print("=" * 70)
        print("\nAnalyzing patients...")
    
    fallback_count = 0
    
    for idx, row in df.iterrows():
        patient = create_patient_from_csv_row(row)
        evaluation = fuzzy_system.evaluate_patient(patient)
        
        # Compter les fallbacks
        if evaluation.get('fallback', False):
            fallback_count += 1
        
        # Récupérer le risque réel
        try:
            actual_risk_str = str(row['Level']).strip().capitalize()
            actual_risk = RiskLevel(actual_risk_str) if actual_risk_str in ['Low','Medium','High'] else None
        except:
            actual_risk = None
        
        predicted_risk = evaluation['risk_level']
        correct = (predicted_risk == actual_risk) if actual_risk else False
        
        result = {
            'patient_id': patient.id,
            'age': patient.age,
            'predicted_risk': predicted_risk,
            'actual_risk': actual_risk,
            'correct': correct,
            'risk_value': evaluation['risk_value'],
            'confidence': evaluation['confidence'],
            'fallback': evaluation.get('fallback', False),
            'rules_applied': evaluation.get('rules_applied', [])
        }
        
        results.append(result)
        
        if verbose and idx < 3:
            print(f"\nPatient {patient.id}:")
            print(f"  Age: {patient.age}")
            print(f"  Smoking: {evaluation['details'].get('smoking', 0):.1f}")
            print(f"  Coughing blood: {evaluation['details'].get('coughing_blood', 0):.1f}")
            print(f"  Predicted: {predicted_risk.value} ({evaluation['risk_value']:.2f}/10)")
            print(f"  Confidence: {evaluation['confidence']:.1f}%")
            if actual_risk:
                print(f"  Actual: {actual_risk.value}")
                print(f"  Correct: {'✓' if correct else '✗'}")
            if evaluation.get('fallback', False):
                print(f"  ⚠️  Fallback system used")
    
    if verbose:
        print(f"\nTotal patients analyzed: {len(df)}")
        print(f"Fallback system used: {fallback_count} times ({fallback_count/len(df)*100:.1f}%)")
    
    return results

def calculate_performance_metrics(results: List[Dict]) -> Dict:
    """Calcule les métriques de performance"""
    total = len(results)
    correct = sum(1 for r in results if r['correct'])
    fallback = sum(1 for r in results if r.get('fallback', False))
    
    # Distributions
    predictions = {'Low': 0, 'Medium': 0, 'High': 0}
    actuals = {'Low': 0, 'Medium': 0, 'High': 0}
    
    for r in results:
        pred = r['predicted_risk'].value
        predictions[pred] = predictions.get(pred, 0) + 1
        
        if r['actual_risk']:
            actual = r['actual_risk'].value
            actuals[actual] = actuals.get(actual, 0) + 1
    
    # Confiance moyenne (seulement pour les non-fallback)
    non_fallback_results = [r for r in results if not r.get('fallback', False)]
    avg_confidence = sum(r['confidence'] for r in non_fallback_results) / len(non_fallback_results) if non_fallback_results else 0
    
    return {
        'total_patients': total,
        'correct_predictions': correct,
        'incorrect_predictions': total - correct,
        'accuracy': (correct / total * 100) if total > 0 else 0,
        'prediction_distribution': predictions,
        'actual_distribution': {k: v for k, v in actuals.items() if v > 0},
        'average_confidence': avg_confidence,
        'fallback_used': fallback,
        'fallback_percentage': (fallback / total * 100) if total > 0 else 0
    }