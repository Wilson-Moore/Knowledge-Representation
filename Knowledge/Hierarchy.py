from dataclasses import dataclass,field

@dataclass
class MRI:
    name: str
    present: bool

@dataclass
class Symptom:
    name: str
    severity: int

@dataclass
class LabTest:
    name: str
    value: float

@dataclass
class Patient:
    id: str
    age: int
    gender: str
    MRIs: list[MRI]=field(default_factory=list)
    symptoms: list[Symptom]=field(default_factory=list)
    lab_tests: list[LabTest]=field(default_factory=list)

@dataclass
class Proposition:
    name: str
    fn: callable[[Patient],bool]