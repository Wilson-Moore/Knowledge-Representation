import pandas as pd
from Logic.Fuzzy_logic.Helpers import analyze_dataset_with_fuzzy, calculate_performance_metrics

def main():
    # Charger les données
    print("Loading dataset...")
    df = pd.read_csv("lung_cancer.csv")
    
    # Analyser
    print("\n" + "="*70)
    print("FUZZY LOGIC ANALYSIS")
    print("="*70)
    
    results = analyze_dataset_with_fuzzy(df, verbose=True)
    
    # Métriques
    metrics = calculate_performance_metrics(results)
    
    # Afficher les résultats
    print("\n" + "="*70)
    print("PERFORMANCE RESULTS")
    print("="*70)
    
    print(f"\n📊 Accuracy: {metrics['accuracy']:.2f}%")
    print(f"   Correct: {metrics['correct_predictions']}/{metrics['total_patients']}")
    
    print(f"\n📈 Predictions:")
    for risk, count in metrics['prediction_distribution'].items():
        perc = (count / metrics['total_patients']) * 100
        print(f"   {risk}: {count} ({perc:.1f}%)")
    
    print(f"\n📊 Actual distribution:")
    for risk, count in metrics['actual_distribution'].items():
        print(f"   {risk}: {count}")
    
    if metrics['fallback_used'] > 0:
        print(f"\n⚠️  Fallback used: {metrics['fallback_used']} ({metrics['fallback_percentage']:.1f}%)")
    else:
        print(f"\n✅ All predictions used fuzzy logic")
    
    print(f"\n🎯 Average confidence: {metrics['average_confidence']:.1f}%")
    
    # Exemples de prédictions
    print("\n" + "="*70)
    print("SAMPLE PREDICTIONS")
    print("="*70)
    
    sample_types = ['High', 'Medium', 'Low']
    for risk_type in sample_types:
        sample = next((r for r in results if r['predicted_risk'].value == risk_type), None)
        if sample:
            print(f"\n{risk_type.upper()} RISK EXAMPLE:")
            print(f"  Patient: {sample['patient_id']}")
            print(f"  Age: {sample['age']}")
            print(f"  Predicted: {sample['predicted_risk'].value}")
            if sample['actual_risk']:
                print(f"  Actual: {sample['actual_risk'].value}")
                print(f"  {'✓ CORRECT' if sample['correct'] else '✗ INCORRECT'}")
            if sample.get('rules_applied'):
                print(f"  Factors: {', '.join(sample['rules_applied'])}")

if __name__ == "__main__":
    main()