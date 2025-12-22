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
            var['low'] = fuzz.trimf(var.universe, [0, 0, 4])
            var['medium'] = fuzz.trimf(var.universe, [3, 5, 7])
            var['high'] = fuzz.trimf(var.universe, [6, 10, 10])
        
        # Âge
        self.age['young'] = fuzz.trapmf(self.age.universe, [0, 0, 25, 35])
        self.age['middle'] = fuzz.trimf(self.age.universe, [30, 45, 60])
        self.age['senior'] = fuzz.trapmf(self.age.universe, [50, 65, 100, 100])
        
        # Risque
        self.risk_level['low'] = fuzz.trimf(self.risk_level.universe, [0, 0, 4])
        self.risk_level['medium'] = fuzz.trimf(self.risk_level.universe, [3, 5, 7])
        self.risk_level['high'] = fuzz.trimf(self.risk_level.universe, [6, 10, 10])
        self.risk_level.defuzzify_method = 'centroid'
        
        # ==================== RÈGLES SIMPLIFIÉES MAIS EFFICACES ====================
        # Basées sur vos règles principales
        rules = [
            # Règles HIGH (d'après vos groupes 1-3)
            ctrl.Rule(self.smoking['high'] & self.air_pollution['high'], self.risk_level['high']),
            ctrl.Rule(self.coughing_blood['high'] & self.chest_pain['high'], self.risk_level['high']),
            ctrl.Rule(self.shortness_breath['high'] & self.weight_loss['high'], self.risk_level['high']),
            ctrl.Rule(self.age['senior'] & self.smoking['high'], self.risk_level['high']),
            
            # Règles MEDIUM (d'après vos groupes 4-6)
            ctrl.Rule(self.smoking['medium'] & self.air_pollution['medium'], self.risk_level['medium']),
            ctrl.Rule(self.chest_pain['medium'] & self.shortness_breath['medium'], self.risk_level['high']),
            ctrl.Rule(self.age['middle'] & self.smoking['medium'], self.risk_level['medium']),
            
            # Règles LOW (d'après vos groupes 7-9)
            ctrl.Rule(self.smoking['low'] & self.air_pollution['low'], self.risk_level['low']),
            ctrl.Rule(self.coughing_blood['low'] & self.chest_pain['low'], self.risk_level['low']),
            ctrl.Rule(self.age['young'] & self.smoking['low'], self.risk_level['low']),
            
            # Règles par défaut
            ctrl.Rule(self.smoking['high'], self.risk_level['medium']),
            ctrl.Rule(self.coughing_blood['high'], self.risk_level['medium']),
            ctrl.Rule(self.age['senior'], self.risk_level['medium']),
            ctrl.Rule(self.age['young'], self.risk_level['low']),
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
        # Mapping simplifié
        symptom_mapping = {
            'smoking': 'smoking_history',
            'air_pollution': 'air_pollution_exposure',
            'coughing_blood': 'coughing_of_blood',
            'chest_pain': 'chest_pain',
            'shortness_breath': 'shortness_of_breath',
            'weight_loss': 'weight_loss'
        }
        
        inputs = {'age': float(patient.age)}
        
        for fuzzy_name, symptom_name in symptom_mapping.items():
            value = 0.0
            for symptom in patient.symptoms:
                if symptom.name == symptom_name:
                    value = float(symptom.severity)
                    break
            inputs[fuzzy_name] = value
        
        return inputs
    
    def _calculate_confidence(self, inputs: Dict, risk_value: float) -> float:
        """Calcule la confiance de la prédiction"""
        confidence = 70.0
        
        # Facteurs de cohérence
        high_indicators = sum(1 for k in ['smoking', 'coughing_blood', 'chest_pain'] 
                             if inputs.get(k, 0) > 7)
        
        if high_indicators >= 2:
            confidence += 20
        elif high_indicators == 1:
            confidence += 10
        
        # Cohérence âge-risque
        age = inputs.get('age', 45)
        if age > 60 and risk_value < 5:
            confidence -= 15
        elif age < 30 and risk_value > 7:
            confidence -= 10
        
        return max(30, min(95, confidence))
    
    def _get_applied_rules(self, inputs: Dict) -> List[str]:
        """Détecte quelles règles pourraient s'appliquer"""
        applied = []
        
        if inputs.get('smoking', 0) > 7:
            applied.append("High smoking")
        
        if inputs.get('coughing_blood', 0) > 7:
            applied.append("Coughing blood")
        
        if inputs.get('age', 0) > 50:
            applied.append("Senior age")
        
        if inputs.get('chest_pain', 0) > 7:
            applied.append("Chest pain")
        
        return applied[:2]
    
    def _fallback_evaluation(self, patient: Patient) -> Dict:
        """Évaluation de secours basée sur un scoring simple"""
        inputs = self._prepare_inputs(patient)
        
        # Scoring simple basé sur vos poids
        score = 0
        score += inputs.get('smoking', 0) * 0.25
        score += inputs.get('air_pollution', 0) * 0.20
        score += inputs.get('coughing_blood', 0) * 0.15
        score += inputs.get('chest_pain', 0) * 0.10
        score += inputs.get('shortness_breath', 0) * 0.10
        score += inputs.get('weight_loss', 0) * 0.10
        
        # Ajustement par âge
        age = inputs.get('age', 45)
        if age > 60:
            score *= 1.2
        elif age < 30:
            score *= 0.8
        
        # Normaliser à 10
        risk_value = min(10, score * 2)
        risk_category = self._crisp_to_risk_level(risk_value)
        
        return {
            'patient': patient,
            'risk_value': risk_value,
            'risk_level': risk_category,
            'confidence': 50.0,
            'details': inputs,
            'rules_applied': ["Fallback scoring system"],
            'fallback': True
        }
    
    def _crisp_to_risk_level(self, risk_value: float) -> RiskLevel:
        """Convertit une valeur numérique en niveau de risque"""
        if risk_value < 3.5:
            return RiskLevel.LOW
        elif risk_value < 6.5:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.HIGH