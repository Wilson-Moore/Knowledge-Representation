from dataclasses import dataclass,field
from typing import List,Dict,Set,Callable,Any
from Knowledge.Hierarchy import Patient,RiskLevel
import pandas as pd

@dataclass(frozen=True, eq=True)
class Proposition:
    name: str
    description: str
    fn: Callable[[Patient],bool]=field(repr=False,compare=False)
    
    def __call__(self,patient: Patient) -> bool:
        return self.fn(patient)

@dataclass(frozen=True)
class PossibleWorld:
    risk_level: RiskLevel
    description: str
    probability: float = 1.0
    
    def __str__(self):
        return f"{self.risk_level.value}: {self.description}"

@dataclass
class ModalLogic:
    
    worlds: List[PossibleWorld]
    accessibility: Dict[PossibleWorld,Set[PossibleWorld]]
    valuation: Dict[PossibleWorld,Set[str]]
    propositions: Dict[str,Proposition]=field(default_factory=dict)

    def __post_init__(self):
        
        if isinstance(self.propositions, list):
            self.propositions = {prop.name: prop for prop in self.propositions}

    def knows(self,world: PossibleWorld,proposition_name: str) -> bool:
        if world not in self.accessibility:
            return False
        
        for accessible_world in self.accessibility[world]:
            if proposition_name not in self.valuation.get(accessible_world,set()):
                return False
        return True
    
    def believes(self,world: PossibleWorld,proposition_name: str) -> bool:
        return proposition_name in self.valuation.get(world,set())
    
    def possibly(self,world: PossibleWorld,proposition_name: str) -> bool:
        if world not in self.accessibility:
            return False
        
        for accessible_world in self.accessibility[world]:
            if proposition_name in self.valuation.get(accessible_world,set()):
                return True
        return False
    
    def necessarily(self,world: PossibleWorld,proposition_name: str) -> bool:
        return self.knows(world,proposition_name)
    
    def evaluate_patient(self,patient: Patient) -> Dict[PossibleWorld,Dict[str,Any]]:
        results={}
        
        patient_true_propositions=set()
        for prop_name,proposition in self.propositions.items():
            try:
                if proposition(patient):
                    patient_true_propositions.add(prop_name)
            except Exception as e:
                print(f"Error evaluating proposition {prop_name}: {e}")
                continue
        
        for world in self.worlds:
            world_propositions=self.valuation.get(world,set())
            
            match=patient_true_propositions.intersection(world_propositions)
            match_score=len(match)
            total_possible=len(world_propositions)
            
            results[world]={
                'world': world,
                'patient_propositions': patient_true_propositions,
                'world_propositions': world_propositions,
                'match_propositions': match,
                'match_score': match_score,
                'match_percentage': (match_score/total_possible*100) if total_possible > 0 else 0,
                'is_possible': self._is_world_possible(world,patient_true_propositions)
            }
        
        return results
    
    def _is_world_possible(self,world: PossibleWorld,patient_propositions: Set[str]) -> bool:
        world_props=self.valuation.get(world,set())
        match=patient_propositions.intersection(world_props)
        return len(match)>=2
    
    def get_most_likely_worlds(self,patient: Patient,top_n: int = 3) -> List[Dict[str, Any]]:
        evaluations=self.evaluate_patient(patient)
        
        possible_worlds={w: d for w, d in evaluations.items() if d['is_possible']}
        
        if not possible_worlds:
            possible_worlds=evaluations
        
        sorted_worlds=sorted(
            possible_worlds.items(),
            key=lambda x: (x[1]['match_percentage'], x[1]['match_score']),
            reverse=True
        )
        
        return [
            {
                'world': world,
                'risk_level': world.risk_level,
                'match_percentage': data['match_percentage'],
                'match_score': data['match_score'],
                'match_propositions': data['match_propositions'],
                'is_possible': data['is_possible']
            }
            for world,data in sorted_worlds[:top_n]
        ]