import sys
import os

# Ajouter le répertoire parent au path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import pandas as pd
from Logic.Fuzzy_logic.Helpers import analyze_dataset_with_fuzzy, calculate_performance_metrics

def test_specific_patients():
    """Tester des patients spécifiques pour debugger"""
    print("🔍 TESTING SPECIFIC PATIENTS")
    print("=" * 60)
    
    # Charger les données
    df = pd.read_csv("data/lung_cancer.csv")
    
    # Chercher des patients avec coughing_blood élevé
    high_coughing = df[df['Coughing of Blood'] >= 8].head(5)
    
    print(f"\nPatients avec Coughing of Blood >= 8:")
    for idx, row in high_coughing.iterrows():
        print(f"\n{row['Patient Id']} (Age: {row['Age']}, Level: {row['Level']}):")
        print(f"  Smoking: {row['Smoking']}")
        print(f"  Coughing of Blood: {row['Coughing of Blood']}")
        print(f"  Chest Pain: {row['Chest Pain']}")
        print(f"  Shortness of Breath: {row['Shortness of Breath']}")
        print(f"  Weight Loss: {row['Weight Loss']}")
    
    return high_coughing

def main():
    # Tester d'abord des patients spécifiques
    test_df = test_specific_patients()
    
    # Analyser avec le moteur flou
    print("\n" + "=" * 70)
    print("FUZZY LOGIC ANALYSIS ON SPECIFIC PATIENTS")
    print("=" * 70)
    
    from Logic.Fuzzy_logic.Engine import FuzzyLungDiseaseSystem
    from Logic.Fuzzy_logic.Helpers import create_patient_from_csv_row
    
    fuzzy_system = FuzzyLungDiseaseSystem()
    
    for idx, row in test_df.iterrows():
        patient = create_patient_from_csv_row(row)
        result = fuzzy_system.evaluate_patient(patient)
        
        print(f"\n📊 RESULT for {patient.id}:")
        print(f"  Actual Level: {row['Level']}")
        print(f"  Predicted: {result['risk_level'].value} ({result['risk_value']:.2f}/10)")
        print(f"  Confidence: {result['confidence']:.1f}%")
        if result.get('rules_applied'):
            print(f"  Rules: {', '.join(result['rules_applied'])}")
    
    # Maintenant analyser tout le dataset
    print("\n" + "=" * 70)
    print("FULL DATASET ANALYSIS")
    print("=" * 70)
    
    df = pd.read_csv("data/lung_cancer.csv")
    results = analyze_dataset_with_fuzzy(df, verbose=False)
    
    # Métriques
    metrics = calculate_performance_metrics(results)
    
    # Afficher les résultats
    print(f"\n📊 Accuracy: {metrics['accuracy']:.2f}%")
    print(f"   Correct: {metrics['correct_predictions']}/{metrics['total_patients']}")
    
    print(f"\n📈 Predictions vs Actual:")
    print(f"   Low: Predicted {metrics['prediction_distribution']['Low']} vs Actual {metrics['actual_distribution'].get('Low', 0)}")
    print(f"   Medium: Predicted {metrics['prediction_distribution']['Medium']} vs Actual {metrics['actual_distribution'].get('Medium', 0)}")
    print(f"   High: Predicted {metrics['prediction_distribution']['High']} vs Actual {metrics['actual_distribution'].get('High', 0)}")
    
    # Analyser les erreurs
    print(f"\n🔍 ERROR ANALYSIS:")
    errors = [r for r in results if not r['correct']]
    
    error_types = {}
    for error in errors[:10]:  # 10 premières erreurs
        actual = error['actual_risk'].value if error['actual_risk'] else 'N/A'
        predicted = error['predicted_risk'].value
        key = f"{actual}->{predicted}"
        error_types[key] = error_types.get(key, 0) + 1
    
    print(f"  Total errors: {len(errors)}")
    print(f"  Error types (top 5):")
    for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    {error_type}: {count}")

if __name__ == "__main__":
    main()