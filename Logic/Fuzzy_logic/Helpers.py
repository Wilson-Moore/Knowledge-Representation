import pandas as pd
from typing import List, Dict
from .Engine import FuzzyLungDiseaseSystem
from Logic.Modal_Logic.Helpers import create_patient_from_csv_row
from Knowledge.Hierarchy import RiskLevel

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