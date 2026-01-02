from dataclasses import dataclass,field
from typing import List,Optional
from enum import Enum

@dataclass(frozen=True)
class Symptom:
    name: str
    severity: int

@dataclass
class Patient:
    id: str
    age: int
    gender: str
    symptoms: List[Symptom]=field(default_factory=list)

    def get_symptom(self,name: str) -> Optional[Symptom]:
        for symptom in self.symptoms:
            if symptom.name==name:
                return symptom
        return None
    
    def has_symptom(self,name: str,min_severity: int=1) -> bool:
        symptom=self.get_symptom(name)
        return symptom is not None and symptom.severity>=min_severity

class RiskLevel(Enum):
    LOW="Low"
    MEDIUM="Medium"
    HIGH="High"