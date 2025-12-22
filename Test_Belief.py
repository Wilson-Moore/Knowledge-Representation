"""
Test simplifié pour Dempster-Shafer
"""
import pandas as pd
from Logic.Belief_Functions.Helpers import (
    analyze_with_belief,
    calculate_metrics,
    print_patient_detail,
    print_summary
)


def test_single_patient():
    """Test sur un seul patient"""
    print("Test sur un patient spécifique...")
    
    # Créer un patient de test (P100 de votre dataset)
    test_data = {
        'Patient Id': 'P100',
        'Age': 35,
        'Smoking': 2,
        'Coughing of Blood': 8,
        'Genetic Risk': 5,
        'chronic Lung Disease': 4,
        'Air Pollution': 4,
        'Chest Pain': 4,
        'Weight Loss': 8,
        'Level': 'High'
    }
    
    # Note: Pour un vrai test, vous devrez créer un objet Patient
    print("(Cette fonction nécessite l'implémentation de create_test_patient)")
    print("Utilisez plutôt test_dataset()")


def test_dataset():
    """Test sur tout le dataset"""
    print("Chargement du dataset...")
    
    try:
        df = pd.read_csv("lung_cancer.csv")
        print(f"Dataset chargé: {len(df)} patients")
    except:
        print("Erreur: fichier lung_cancer.csv non trouvé")
        print("Assurez-vous qu'il est dans le dossier courant")
        return
    
    print("\n" + "="*60)
    print("ANALYSE COMPLÈTE - DEMPSTER-SHAFER")
    print("="*60)
    
    # Analyser
    results = analyze_with_belief(df, verbose=True)
    
    # Résumé
    print_summary(results)
    
    # Détail d'un patient
    if results:
        print("\n" + "="*60)
        print("DÉTAIL D'UN PATIENT")
        print("="*60)
        print_patient_detail(results, results[0]['patient_id'])
    
    # Analyse par risque
    print("\n" + "="*60)
    print("ANALYSE PAR NIVEAU DE RISQUE")
    print("="*60)
    
    for risk in ['Low', 'Medium', 'High']:
        risk_results = [r for r in results if r['predicted'].value == risk]
        if risk_results:
            correct = sum(1 for r in risk_results if r['correct'])
            total = len(risk_results)
            acc = (correct / total * 100) if total > 0 else 0
            
            print(f"\n{risk.upper()}:")
            print(f"  Nombre: {total}")
            print(f"  Précision: {acc:.1f}% ({correct}/{total})")
            
            # Confiance moyenne pour cette catégorie
            avg_conf = sum(r['confidence'] for r in risk_results) / total
            print(f"  Confiance moyenne: {avg_conf:.3f}")
    
    # Cas difficiles (faible confiance)
    print("\n" + "="*60)
    print("CAS À FAIBLE CONFIANCE (< 0.5)")
    print("="*60)
    
    low_conf = [r for r in results if r['confidence'] < 0.5]
    if low_conf:
        print(f"\n{len(low_conf)} cas à faible confiance:")
        for r in low_conf[:3]:  # Afficher 3 exemples
            print(f"  Patient {r['patient_id']}: "
                  f"confiance={r['confidence']:.3f}, "
                  f"prédit={r['predicted'].value}")
    else:
        print("\nAucun cas à faible confiance détecté.")
    
    # Performance finale
    metrics = calculate_metrics(results)
    print("\n" + "="*60)
    print("PERFORMANCE FINALE")
    print("="*60)
    
    print(f"\n✅ Précision: {metrics['accuracy']:.1f}%")
    print(f"📊 Distribution: {metrics['predictions']}")
    print(f"🎯 Confiance: {metrics['avg_confidence']:.3f}")


def quick_test():
    """Test rapide"""
    print("\n" + "="*50)
    print("TEST RAPIDE DEMPSTER-SHAFER")
    print("="*50)
    
    # Créer un mini-dataset de test
    test_data = {
        'Patient Id': ['P1', 'P2', 'P3'],
        'Age': [33, 35, 45],
        'Smoking': [3, 2, 7],
        'Coughing of Blood': [4, 8, 3],
        'Genetic Risk': [3, 5, 6],
        'chronic Lung Disease': [2, 4, 7],
        'Air Pollution': [2, 4, 6],
        'Chest Pain': [2, 4, 5],
        'Weight Loss': [4, 8, 3],
        'Level': ['Low', 'High', 'Medium']
    }
    
    df = pd.DataFrame(test_data)
    print(f"\nDataset de test: {len(df)} patients")
    
    results = analyze_with_belief(df, verbose=True)
    
    if results:
        print("\nRésultats du test:")
        for r in results:
            status = "✓" if r['correct'] else "✗"
            print(f"  {r['patient_id']}: {r['predicted'].value} "
                  f"({r['actual'].value if r['actual'] else '?'}) {status}")


def main():
    test_dataset()

    
if __name__ == "__main__":
    main()