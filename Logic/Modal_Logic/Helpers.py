from typing import List,Dict
from Knowledge.Hierarchy import Symptom,Patient,RiskLevel
from Logic.Modal_Logic.Engine import Proposition,ModalLogic,PossibleWorld
import pandas as pd

def create_lung_disease_propositions() -> List[Proposition]:

    propositions=[
        Proposition(
            name="young",
            description="Patient is young (age < 30)",
            fn=lambda p: p.age<30
        ),

        Proposition(
            name="middle_aged",
            description="Patient is middle-aged (30-50)",
            fn=lambda p: 30<=p.age<=50
        ),

        Proposition(
            name="senior",
            description="Patient is senior (age > 50)",
            fn=lambda p: p.age>50
        ),

        Proposition(
            name="coughing_blood",
            description="Has coughing of blood",
            fn=lambda p: p.has_symptom("coughing_blood",1)
        ),

        Proposition(
            name="chest_pain",
            description="Has chest pain (severity >= 5)",
            fn=lambda p: p.has_symptom("chest_pain",5)
        ),

        Proposition(
            name="shortness_of_breath",
            description="Has shortness of breath (severity >= 6)",
            fn=lambda p: p.has_symptom("shortness_of_breath",6)
        ),

        Proposition(
            name="light_fatigue",
            description="Has fatigue (severity >= 6)",
            fn=lambda p: p.has_symptom("fatigue",1)
        ),

        Proposition(
            name="fatigue",
            description="Has fatigue (severity >= 6)",
            fn=lambda p: p.has_symptom("fatigue",3)
        ),

        Proposition(
            name="weight_loss",
            description="Has unexplained weight loss",
            fn=lambda p: p.has_symptom("weight_loss",2)
        ),

        Proposition(
            name="wheezing",
            description="Has wheezing",
            fn=lambda p: p.has_symptom("wheezing",1)
        ),

        Proposition(
            name="swallowing_difficulty",
            description="Difficulty swallowing food",
            fn=lambda p: p.has_symptom("swallowing_difficulty",2)
        ),

        Proposition(
            name="smoker",
            description="Current or former smoker",
            fn=lambda p: p.has_symptom("smoking_history",1)
        ),

        Proposition(
            name="heavy_smoker",
            description="Heavy smoker (smoking severity >= 5)",
            fn=lambda p: p.has_symptom("smoking_history",5)
        ),

        Proposition(
            name="alcohol_use",
            description="Alcohol abuse (alcohol use >= 4)",
            fn=lambda p: p.has_symptom("alcohol_use",4)
        ),

        Proposition(
            name="alcoholic",
            description="Alcoholic (alcohol_use >= 6)",
            fn=lambda p: p.has_symptom("alcohol_use",6)
        ),

        Proposition(
            name="light_passive_smoker",
            description="Exposed to passive smoking",
            fn=lambda p: p.has_symptom("passive_smoke_exposure",2)
        ),

        Proposition(
            name="heavy_passive_smoker",
            description="Exposed to alot of passive smoking",
            fn=lambda p: p.has_symptom("passive_smoke_exposure",7)
        ),

        Proposition(
            name="occupational_hazards",
            description="Exposed to occupational hazards",
            fn=lambda p: p.has_symptom("occupational_exposure",4)
        ),

        Proposition(
            name="air_pollution",
            description="High exposure to air pollution",
            fn=lambda p: p.has_symptom("air_pollution_exposure",4)
        ),

        Proposition(
            name="frequent_cold",
            description="Frequent cold >= 4",
            fn=lambda p: p.has_symptom("frequent_cold", 4),
        ),

        Proposition(
            name="dry_cough",
            description="Dry cough >= 4",
            fn=lambda p: p.has_symptom("dry_cough", 4),
        ),

        Proposition(
            name="snoring",
            description="Snores",
            fn=lambda p: p.has_symptom("snoring", 1),
        ),
    ]
    
    return propositions


def create_lung_disease_modal_model() -> ModalLogic:
    
    low_risk_world=PossibleWorld(
        risk_level=RiskLevel.LOW,
        description="Low risk of lung disease"
    )
    
    medium_risk_world=PossibleWorld(
        risk_level=RiskLevel.MEDIUM,
        description="Medium risk of lung disease"
    )
    
    high_risk_world=PossibleWorld(
        risk_level=RiskLevel.HIGH,
        description="High risk of lung disease"
    )
    
    worlds=[low_risk_world,medium_risk_world,high_risk_world]
    
    accessibility={
        low_risk_world: {low_risk_world,medium_risk_world},
        medium_risk_world: {medium_risk_world,low_risk_world,high_risk_world},
        high_risk_world: {high_risk_world}
    }
    
    propositions=create_lung_disease_propositions()
    
    valuation={
        low_risk_world: {"young","light_passive_smoker","occupational_hazards","snoring","air_pollution_exposure","light_fatigue"},
        medium_risk_world: {"middle_aged","smoker","alcohol_use","weight_loss","shortness_of_breath","dry_cough","fatigue"},
        high_risk_world: {"senior","heavy_passive_smoker","alcoholic","heavy_smoker","coughing_blood","chest_pain","wheezing","swallowing_difficulty"}
    }
    
    propositions_dict={prop.name: prop for prop in propositions}
    
    return ModalLogic(worlds=worlds,accessibility=accessibility,valuation=valuation,propositions=propositions_dict)

def create_patient_from_csv_row(row: pd.Series) -> Patient:
    symptoms=[]
    
    symptom_mapping={
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
    
    for csv_col,symptom_name in symptom_mapping.items():
        severity=int(row[csv_col])
        symptoms.append(Symptom(name=symptom_name, severity=severity))
    
    smoking_severity=int(row['Smoking'])
    if smoking_severity>=1:
        symptoms.append(Symptom(name="smoking_history",severity=smoking_severity))
    
    if int(row['Passive Smoker'])>=1:
        symptoms.append(Symptom(name="passive_smoke_exposure",severity=int(row['Passive Smoker'])))
    
    return Patient(id=row['Patient Id'],
        age=int(row['Age']),
        gender="M" if int(row['Gender'])==1 else "F",
        symptoms=symptoms
    )


def analyze_dataset_with_kripke(df: pd.DataFrame) -> List[Dict]:
    
    model=create_lung_disease_modal_model()
    results=[]
    
    print("Analyzing patients with Kripke semantics...\n")
    
    for idx,row in df.iterrows():
        patient=create_patient_from_csv_row(row)
        
        likely_worlds=model.get_most_likely_worlds(patient, top_n=3)
        
        try:
            actual_risk=RiskLevel(row['Level'])
        except ValueError:
            level_str=str(row['Level']).strip().capitalize()
            if level_str in ['Low','Medium','High']:
                actual_risk=RiskLevel(level_str)
            else:
                print(f"Warning: Unknown risk level '{row['Level']}' for patient {patient.id}")
                continue
        
        predicted_risk=likely_worlds[0]['risk_level'] if likely_worlds else None
        correct=predicted_risk==actual_risk
        
        result={
            'patient_id': patient.id,
            'age': patient.age,
            'gender': patient.gender,
            'predicted_risk': predicted_risk,
            'actual_risk': actual_risk,
            'correct': correct,
            'top_predictions': likely_worlds,
            'patient': patient
        }
        
        results.append(result)
        
        # if idx<5:
        #     print(f"Patient: {patient.id}")
        #     print(f"  Age: {patient.age}, Gender: {patient.gender}")
        #     print(f"  Predicted: {predicted_risk.value if predicted_risk else 'Unknown'}")
        #     print(f"  Actual: {actual_risk.value}")
        #     print(f"  Correct: {'yes' if correct else 'no'}")
        #     print(f"  Top predictions:")
        #     for pred in likely_worlds[:2]:
        #         print(f"    - {pred['risk_level'].value}: {pred['match_percentage']:.1f}% match")
        #         if pred['match_propositions']:
        #             print(f"      Matching propositions: {', '.join(pred['match_propositions'])}")
        #     print()
    
    return results


def demonstrate_modal_operators(model: ModalLogic,patient: Patient):
    
    print("="*60)
    print("MODAL LOGIC DEMONSTRATION")
    print("="*60)
    
    likely_worlds=model.get_most_likely_worlds(patient,top_n=1)
    if not likely_worlds:
        print("Could not determine likely world")
        return
    
    current_world=likely_worlds[0]['world']
    
    print(f"\nPatient {patient.id} is most likely in: {current_world.description}")
    print(f"Risk Level: {current_world.risk_level.value}")
    
    test_proposition_names=["coughing_blood","chest_pain","shortness_of_breath","young"]
    
    print("\nModal Analysis:")
    print("-" * 40)
    
    for prop_name in test_proposition_names:
        if prop_name not in model.propositions:
            continue
            
        prop=model.propositions[prop_name]
        
        is_true_for_patient=prop(patient)
        
        print(f"\nProposition: {prop_name} ({prop.description})")
        print(f"  True for patient: {is_true_for_patient}")
        
        believed=model.believes(current_world,prop_name)
        print(f"  Believes in current world: {believed}")
        
        known=model.knows(current_world,prop_name)
        print(f"  Known (true in all accessible worlds): {known}")
        
        possible=model.possibly(current_world, prop_name)
        print(f"  Possible (true in some accessible world): {possible}")
        
        necessary=model.necessarily(current_world, prop_name)
        print(f"  Necessary: {necessary}")