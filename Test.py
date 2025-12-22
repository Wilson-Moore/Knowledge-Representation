import pandas as pd
from Logic.Modal_Logic.Helpers import analyze_dataset_with_kripke,create_lung_disease_modal_model,demonstrate_modal_operators

df=pd.read_csv("lung_cancer.csv")

print("LUNG DISEASE RISK ASSESSMENT USING KRIPKE SEMANTICS")
print("="*60)

results = analyze_dataset_with_kripke(df)

# Calculate accuracy
if results:
    correct_predictions = sum(1 for r in results if r['correct'])
    total_patients = len(results)
    accuracy = (correct_predictions / total_patients * 100) if total_patients > 0 else 0
    
    print(f"\nOverall Accuracy: {accuracy:.1f}% ({correct_predictions}/{total_patients})")
    
    # Demonstrate modal operators on first patient
    first_patient = results[0]['patient']
    model = create_lung_disease_modal_model()
    demonstrate_modal_operators(model, first_patient)

# Show Kripke model structure
print("\n" + "="*60)
print("KRIPKE MODEL STRUCTURE")
print("="*60)

model = create_lung_disease_modal_model()
print(f"\nNumber of worlds: {len(model.worlds)}")
print(f"Number of propositions: {len(model.propositions)}")

print("\nWorlds:")
for world in model.worlds:
    num_props = len(model.valuation.get(world, set()))
    print(f"  - {world.risk_level.value}: {world.description} ({num_props} propositions)")

print("\nAccessibility Relations:")
for world in model.worlds:
    accessible = model.accessibility.get(world, set())
    accessible_names = [w.risk_level.value for w in accessible]
    print(f"  {world.risk_level.value} → {', '.join(accessible_names)}")

print("\nValuation (Sample):")
for world in model.worlds:
    props = model.valuation.get(world, set())
    if props:
        sample_props = list(props)[:10]  # Show first 10
        print(f"  {world.risk_level.value}: {', '.join(sample_props)}" + 
              ("..." if len(props) > 10 else ""))