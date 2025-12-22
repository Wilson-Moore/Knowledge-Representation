"""
Helpers simplifiés pour Dempster-Shafer
"""
import pandas as pd
from typing import List, Dict
from .Engine import DSBalanced
from Logic.Modal_Logic.Helpers import create_patient_from_csv_row
from Knowledge.Hierarchy import RiskLevel


def analyze_with_belief(df: pd.DataFrame, verbose: bool = False) -> List[Dict]:
    """Analyse le dataset avec Dempster-Shafer"""
    system = DSBalanced()
    results = []
    
    if verbose:
        print("Analyse avec Dempster-Shafer...")
    
    for idx, row in df.iterrows():
        patient = create_patient_from_csv_row(row)
        result = system.evaluate(patient)
        
        # Risque réel
        try:
            actual_str = str(row['Level']).strip().capitalize()
            actual = RiskLevel(actual_str) if actual_str in ['Low','Medium','High'] else None
        except:
            actual = None
        
        # Comparaison
        predicted = result['predicted']
        correct = (predicted == actual) if actual else False
        
        results.append({
            'patient_id': patient.id,
            'age': patient.age,
            'predicted': predicted,
            'actual': actual,
            'correct': correct,
            'belief': result['belief'],
            'confidence': result['confidence']
        })
        
        if verbose and idx < 2:
            print(f"\nPatient {patient.id}:")
            print(f"  Prédit: {predicted.value}")
            print(f"  Croyance: {result['belief']}")
            if actual:
                print(f"  Réel: {actual.value}")
                print(f"  Correct: {'✓' if correct else '✗'}")
    
    return results


def calculate_metrics(results: List[Dict]) -> Dict:
    """Calcule les métriques de performance"""
    total = len(results)
    correct = sum(1 for r in results if r['correct'])
    
    # Distribution
    pred_dist = {'Low': 0, 'Medium': 0, 'High': 0}
    act_dist = {'Low': 0, 'Medium': 0, 'High': 0}
    
    for r in results:
        pred = r['predicted'].value
        pred_dist[pred] += 1
        
        if r['actual']:
            act = r['actual'].value
            act_dist[act] += 1
    
    # Moyennes
    avg_conf = sum(r['confidence'] for r in results) / total if total > 0 else 0
    
    return {
        'total': total,
        'correct': correct,
        'accuracy': (correct / total * 100) if total > 0 else 0,
        'predictions': pred_dist,
        'actuals': act_dist,
        'avg_confidence': avg_conf
    }


def print_patient_detail(results: List[Dict], patient_id: str):
    """Affiche les détails d'un patient"""
    for r in results:
        if r['patient_id'] == patient_id:
            print(f"\nPatient {patient_id}:")
            print(f"  Âge: {r['age']}")
            print(f"  Prédit: {r['predicted'].value}")
            print(f"  Croyance: Low={r['belief']['Low']:.3f}, "
                  f"Medium={r['belief']['Medium']:.3f}, "
                  f"High={r['belief']['High']:.3f}")
            print(f"  Confiance: {r['confidence']:.3f}")
            if r['actual']:
                print(f"  Réel: {r['actual'].value}")
                print(f"  Correct: {'✓' if r['correct'] else '✗'}")
            return
    
    print(f"Patient {patient_id} non trouvé")


def print_summary(results: List[Dict]):
    """Affiche un résumé"""
    metrics = calculate_metrics(results)
    
    print("\n" + "="*50)
    print("RÉSUMÉ DEMPSTER-SHAFER")
    print("="*50)
    
    print(f"\n📊 Performance:")
    print(f"  Précision: {metrics['accuracy']:.1f}%")
    print(f"  Corrects: {metrics['correct']}/{metrics['total']}")
    
    print(f"\n📈 Prédictions:")
    for risk, count in metrics['predictions'].items():
        perc = (count / metrics['total']) * 100
        print(f"  {risk}: {count} ({perc:.1f}%)")
    
    print(f"\n🎯 Confiance moyenne: {metrics['avg_confidence']:.3f}")
    
    # Afficher 2 exemples
    print(f"\n📋 Exemples:")
    for i, r in enumerate(results[:2], 1):
        print(f"\n  {i}. Patient {r['patient_id']}:")
        print(f"     Prédit: {r['predicted'].value}")
        if r['actual']:
            print(f"     Réel: {r['actual'].value}")
            print(f"     {'✓ Correct' if r['correct'] else '✗ Incorrect'}")