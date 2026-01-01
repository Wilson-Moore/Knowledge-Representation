import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from typing import Dict, List
from Knowledge.Hierarchy import Patient, RiskLevel

class FuzzyLungDiseaseSystem:
    def __init__(self):
        self.system = None
        self.simulation = None
        self.setup_fuzzy_system()
    
    def setup_fuzzy_system(self):
        """Configure le système flou simplifié mais efficace"""
        
        # ==================== VARIABLES D'ENTRÉE SIMPLIFIÉES ====================
        # Variables principales basées sur vos règles
        self.smoking = ctrl.Antecedent(np.arange(0, 11, 1), 'smoking')
        self.air_pollution = ctrl.Antecedent(np.arange(0, 11, 1), 'air_pollution')
        self.coughing_blood = ctrl.Antecedent(np.arange(0, 11, 1), 'coughing_blood')
        self.chest_pain = ctrl.Antecedent(np.arange(0, 11, 1), 'chest_pain')
        self.shortness_breath = ctrl.Antecedent(np.arange(0, 11, 1), 'shortness_breath')
        self.weight_loss = ctrl.Antecedent(np.arange(0, 11, 1), 'weight_loss')
        self.age = ctrl.Antecedent(np.arange(0, 101, 1), 'age')
        
        # ==================== VARIABLE DE SORTIE ====================
        self.risk_level = ctrl.Consequent(np.arange(0, 11, 1), 'risk_level')
        
        # ==================== FONCTIONS D'APPARTENANCE SIMPLIFIÉES ====================
        # Toutes les variables ont la même échelle pour simplifier
        for var in [self.smoking, self.air_pollution, self.coughing_blood, 
                    self.chest_pain, self.shortness_breath, self.weight_loss]:
            var['low'] = fuzz.trimf(var.universe, [0, 0, 3])    # low: 0-3
            var['medium'] = fuzz.trimf(var.universe, [2, 5, 8]) # medium: 2-8  
            var['high'] = fuzz.trimf(var.universe, [6, 10, 10]) # high: 6-10
        
        # Âge
        self.age['young'] = fuzz.trapmf(self.age.universe, [0, 0, 25, 35])
        self.age['middle'] = fuzz.trimf(self.age.universe, [30, 45, 60])
        self.age['senior'] = fuzz.trapmf(self.age.universe, [50, 65, 100, 100])
        
        # Risque
        self.risk_level['low'] = fuzz.trimf(self.risk_level.universe, [0, 0, 4])
        self.risk_level['medium'] = fuzz.trimf(self.risk_level.universe, [3, 5, 7])
        self.risk_level['high'] = fuzz.trimf(self.risk_level.universe, [6, 10, 10])
        self.risk_level.defuzzify_method = 'centroid'
        
        # ==================== RÈGLES CORRIGÉES POUR ÊTRE PLUS SENSIBLES ====================
        # Règles HIGH - symptômes graves seuls peuvent donner HIGH
        rules = [
            # Règles HIGH (symptômes graves)
            ctrl.Rule(self.coughing_blood['high'], self.risk_level['high']),  # Coughing blood seul -> HIGH
            ctrl.Rule(self.smoking['high'] & self.age['senior'], self.risk_level['high']),
            ctrl.Rule(self.smoking['high'] & self.air_pollution['high'], self.risk_level['high']),
            ctrl.Rule(self.coughing_blood['high'] & self.chest_pain['high'], self.risk_level['high']),
            ctrl.Rule(self.shortness_breath['high'] & self.weight_loss['high'], self.risk_level['high']),
            
            # Règles MEDIUM
            ctrl.Rule(self.smoking['medium'] & self.air_pollution['medium'], self.risk_level['medium']),
            ctrl.Rule(self.chest_pain['medium'] & self.shortness_breath['medium'], self.risk_level['medium']),
            ctrl.Rule(self.age['middle'] & self.smoking['medium'], self.risk_level['medium']),
            ctrl.Rule(self.coughing_blood['medium'], self.risk_level['medium']),
            ctrl.Rule(self.chest_pain['medium'], self.risk_level['medium']),
            ctrl.Rule(self.shortness_breath['medium'] & self.weight_loss['medium'], self.risk_level['medium']),
            
            # Règles LOW
            ctrl.Rule(self.smoking['low'] & self.air_pollution['low'], self.risk_level['low']),
            ctrl.Rule(self.coughing_blood['low'] & self.chest_pain['low'], self.risk_level['low']),
            ctrl.Rule(self.age['young'] & self.smoking['low'], self.risk_level['low']),
            
            # Règles par défaut (atténuées)
            ctrl.Rule(self.smoking['high'], self.risk_level['medium']),
            ctrl.Rule(self.age['senior'], self.risk_level['medium']),
            ctrl.Rule(self.age['young'], self.risk_level['low']),
            
            # Règle de base: si aucun symptôme -> LOW
            ctrl.Rule(self.smoking['low'] & self.coughing_blood['low'] & 
                     self.chest_pain['low'] & self.shortness_breath['low'], 
                     self.risk_level['low']),
        ]
        
        # Création du système
        self.system = ctrl.ControlSystem(rules)
        self.simulation = ctrl.ControlSystemSimulation(self.system)
    
    def evaluate_patient(self, patient: Patient) -> Dict:
        """Évalue un patient avec le système flou"""
        try:
            # Préparer les entrées
            inputs = self._prepare_inputs(patient)
            
            # S'assurer que toutes les entrées sont dans les bornes
            for key, value in inputs.items():
                if key == 'age':
                    inputs[key] = max(0, min(100, float(value)))
                else:
                    inputs[key] = max(0, min(10, float(value)))
            
            # Vérifier si la simulation existe
            if not self.simulation:
                self.setup_fuzzy_system()
            
            # Afficher les valeurs importantes
            print(f"\n[ENGINE] Patient {patient.id}:")
            print(f"  Age: {inputs['age']}")
            print(f"  Smoking: {inputs['smoking']:.1f} {'(HIGH)' if inputs['smoking'] > 6 else '(MEDIUM)' if inputs['smoking'] > 2 else '(LOW)'}")
            print(f"  Coughing blood: {inputs['coughing_blood']:.1f} {'(HIGH)' if inputs['coughing_blood'] > 6 else '(MEDIUM)' if inputs['coughing_blood'] > 2 else '(LOW)'}")
            print(f"  Chest pain: {inputs['chest_pain']:.1f} {'(HIGH)' if inputs['chest_pain'] > 6 else '(MEDIUM)' if inputs['chest_pain'] > 2 else '(LOW)'}")
            
            # Définir les entrées
            self.simulation.input['smoking'] = inputs['smoking']
            self.simulation.input['air_pollution'] = inputs['air_pollution']
            self.simulation.input['coughing_blood'] = inputs['coughing_blood']
            self.simulation.input['chest_pain'] = inputs['chest_pain']
            self.simulation.input['shortness_breath'] = inputs['shortness_breath']
            self.simulation.input['weight_loss'] = inputs['weight_loss']
            self.simulation.input['age'] = inputs['age']
            
            # Exécuter le calcul
            self.simulation.compute()
            
            # Obtenir le résultat
            risk_value = float(self.simulation.output['risk_level'])
            risk_category = self._crisp_to_risk_level(risk_value)
            
            # Calculer la confiance
            confidence = self._calculate_confidence(inputs, risk_value)
            
            print(f"  -> Risk: {risk_value:.2f}/10 = {risk_category.value}")
            
            return {
                'patient': patient,
                'risk_value': risk_value,
                'risk_level': risk_category,
                'confidence': confidence,
                'details': inputs,
                'rules_applied': self._get_applied_rules(inputs),
                'fallback': False
            }
            
        except Exception as e:
            # En cas d'erreur, utiliser la méthode de secours
            print(f"Fuzzy system error for patient {patient.id}: {str(e)[:100]}")
            return self._fallback_evaluation(patient)
    
    def _prepare_inputs(self, patient: Patient) -> Dict[str, float]:
        """Prépare les entrées depuis le patient"""
        # MAPPING CORRIGÉ - correspond aux noms de colonnes CSV
        symptom_mapping = {
            'smoking': 'Smoking',
            'air_pollution': 'Air Pollution',
            'coughing_blood': 'Coughing of Blood',
            'chest_pain': 'Chest Pain',
            'shortness_breath': 'Shortness of Breath',
            'weight_loss': 'Weight Loss'
        }
        
        inputs = {'age': float(patient.age)}
        
        for fuzzy_name, symptom_name in symptom_mapping.items():
            value = 0.0
            for symptom in patient.symptoms:
                # Recherche exacte du nom du symptôme
                if symptom.name == symptom_name:
                    value = float(symptom.severity)
                    break
            inputs[fuzzy_name] = value
        
        return inputs
    
    def _calculate_confidence(self, inputs: Dict, risk_value: float) -> float:
        """Calcule la confiance de la prédiction"""
        confidence = 70.0
        
        # Facteurs de cohérence - PLUS SENSIBLE
        high_indicators = sum(1 for k in ['smoking', 'coughing_blood', 'chest_pain'] 
                             if inputs.get(k, 0) > 6)  # Seuil abaissé à 6
        
        if high_indicators >= 2:
            confidence += 25
        elif high_indicators == 1:
            confidence += 15
        
        # Cohérence âge-risque
        age = inputs.get('age', 45)
        if age > 60 and risk_value < 5:
            confidence -= 10
        elif age < 30 and risk_value > 7:
            confidence -= 5
        
        return max(50, min(95, confidence))
    
    def _get_applied_rules(self, inputs: Dict) -> List[str]:
        """Détecte quelles règles pourraient s'appliquer"""
        applied = []
        
        # Règles HIGH
        if inputs.get('coughing_blood', 0) > 6:
            applied.append("Coughing blood (HIGH)")
        elif inputs.get('coughing_blood', 0) > 3:
            applied.append("Coughing blood (MEDIUM)")
        
        if inputs.get('smoking', 0) > 6:
            applied.append("Smoking (HIGH)")
        elif inputs.get('smoking', 0) > 3:
            applied.append("Smoking (MEDIUM)")
        
        if inputs.get('chest_pain', 0) > 6:
            applied.append("Chest pain (HIGH)")
        
        if inputs.get('age', 0) > 50:
            applied.append("Senior age")
        elif inputs.get('age', 0) < 30:
            applied.append("Young age")
        
        return applied[:3]
    
    def _fallback_evaluation(self, patient: Patient) -> Dict:
        """Évaluation de secours basée sur un scoring simple"""
        inputs = self._prepare_inputs(patient)
        
        # Scoring simple avec pondérations réalistes
        score = 0
        score += inputs.get('smoking', 0) * 0.3  # Augmenté
        score += inputs.get('air_pollution', 0) * 0.15
        score += inputs.get('coughing_blood', 0) * 0.25  # Augmenté
        score += inputs.get('chest_pain', 0) * 0.15
        score += inputs.get('shortness_breath', 0) * 0.10
        score += inputs.get('weight_loss', 0) * 0.05
        
        # Ajustement par âge
        age = inputs.get('age', 45)
        if age > 60:
            score *= 1.3  # Augmenté
        elif age > 45:
            score *= 1.1
        elif age < 30:
            score *= 0.8
        
        # Normaliser à 10
        risk_value = min(10, score)
        risk_category = self._crisp_to_risk_level(risk_value)
        
        return {
            'patient': patient,
            'risk_value': risk_value,
            'risk_level': risk_category,
            'confidence': 60.0,
            'details': inputs,
            'rules_applied': ["Fallback scoring system"],
            'fallback': True
        }
    
    def _crisp_to_risk_level(self, risk_value: float) -> RiskLevel:
        """Convertit une valeur numérique en niveau de risque"""
        # Seuils ajustés pour être plus sensibles
        if risk_value < 3:  # Low: 0-3.0
            return RiskLevel.LOW
        elif risk_value < 6.5:  # Medium: 3.0-6.5
            return RiskLevel.MEDIUM
        else:  # High: 6.5-10
            return RiskLevel.HIGH