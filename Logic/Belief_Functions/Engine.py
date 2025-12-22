"""
Engine Dempster-Shafer équilibré - Simple mais complet
"""
from typing import Dict, List, Tuple
from enum import Enum
from Knowledge.Hierarchy import Patient, RiskLevel


class DSBalanced:
    """Bon compromis simplicité/fonctionnalité"""
    
    def __init__(self):
        # 3 sources simples
        self.sources = {
            'symptoms': ['coughing_of_blood', 'chest_pain', 'weight_loss'],
            'exposure': ['smoking', 'air_pollution'],
            'history': ['genetic_risk', 'chronic_lung_disease']
        }
        
        # Hypothèses
        self.H = Enum('H', 'LOW MEDIUM HIGH')
    
    def evaluate(self, patient: Patient) -> Dict:
        """Évalue un patient"""
        # Données du patient
        data = self._get_patient_data(patient)
        
        # Masses pour chaque source
        masses = []
        for src_name, indicators in self.sources.items():
            mass = self._source_mass(data, indicators)
            masses.append(mass)
        
        # Combinaison
        final_mass = self._combine_masses(masses)
        
        # Décision
        risk, confidence = self._make_decision(final_mass)
        
        return {
            'patient': patient,
            'predicted': risk,
            'belief': self._get_belief(final_mass),
            'confidence': confidence,
            'method': 'Dempster-Shafer'
        }
    
    def _get_patient_data(self, patient: Patient) -> Dict[str, float]:
        """Extrait données normalisées"""
        data = {}
        for symptom in patient.symptoms:
            data[symptom.name] = symptom.severity / 10.0
        return data
    
    def _source_mass(self, data: Dict, indicators: List[str]) -> Dict[Tuple, float]:
        """Calcule masse pour une source"""
        # Score moyen
        scores = [data.get(i, 0.0) for i in indicators]
        score = sum(scores) / max(len(scores), 1)
        
        if score < 0.4:
            return {(self.H.LOW,): 0.6, (self.H.LOW, self.H.MEDIUM): 0.3, (self.H.LOW, self.H.MEDIUM, self.H.HIGH): 0.1}
        elif score < 0.7:
            return {(self.H.MEDIUM,): 0.4, (self.H.MEDIUM, self.H.HIGH): 0.3, (self.H.LOW, self.H.MEDIUM, self.H.HIGH): 0.3}
        else:
            return {(self.H.HIGH,): 0.7, (self.H.MEDIUM, self.H.HIGH): 0.2, (self.H.LOW, self.H.MEDIUM, self.H.HIGH): 0.1}
    
    def _combine_masses(self, masses: List[Dict]) -> Dict:
        """Combine avec Dempster simplifié"""
        if not masses:
            return {(self.H.LOW, self.H.MEDIUM, self.H.HIGH): 1.0}
        
        current = masses[0]
        for mass in masses[1:]:
            new = {}
            for (setA, mA) in current.items():
                for (setB, mB) in mass.items():
                    # Intersection
                    inter = tuple(set(setA).intersection(set(setB)))
                    if inter:
                        new[inter] = new.get(inter, 0.0) + mA * mB
            
            # Normaliser
            total = sum(new.values())
            if total > 0:
                current = {k: v/total for k, v in new.items()}
        
        return current
    
    def _get_belief(self, mass: Dict) -> Dict[str, float]:
        """Calcule croyance"""
        belief = {'Low': 0.0, 'Medium': 0.0, 'High': 0.0}
        
        for subset, value in mass.items():
            if self.H.LOW in subset:
                belief['Low'] += value
            if self.H.MEDIUM in subset:
                belief['Medium'] += value
            if self.H.HIGH in subset:
                belief['High'] += value
        
        return belief
    
    def _make_decision(self, mass: Dict) -> Tuple[RiskLevel, float]:
        """Prend décision"""
        belief = self._get_belief(mass)
        
        # Chercher max
        max_risk = max(belief, key=belief.get)
        confidence = belief[max_risk]
        
        return RiskLevel(max_risk), confidence