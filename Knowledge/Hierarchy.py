from dataclasses import dataclass,field
from typing import List,Callable,Optional
from enum import Enum

@dataclass(frozen=True)
class MRI:
    name: str
    present: bool

@dataclass(frozen=True)
class Symptom:
    name: str
    severity: int

@dataclass(frozen=True)
class LabTest:
    name: str
    value: float
    unit: str=""

@dataclass
class Patient:
    id: str
    age: int
    gender: str
    MRIs: List[MRI]=field(default_factory=list)
    symptoms: List[Symptom]=field(default_factory=list)
    lab_tests: List[LabTest]=field(default_factory=list)

    def get_symptom(self,name: str) -> Optional[Symptom]:
        for symptom in self.symptoms:
            if symptom.name==name:
                return symptom
        return None
    
    def has_symptom(self,name: str,min_severity: int=1) -> bool:
        symptom=self.get_symptom(name)
        return symptom is not None and symptom.severity>=min_severity
    
    def get_lab_value(self,name: str) -> Optional[float]:
        for test in self.lab_tests:
            if test.name==name:
                return test.value
        return None

class RiskLevel(Enum):
    LOW="Low"
    MEDIUM="Medium"
    HIGH="High"