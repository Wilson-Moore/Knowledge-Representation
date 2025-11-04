from dataclasses import dataclass,field

@dataclass
class Symptom:
    name: str

@dataclass
class Test:
    name: str
    value: float

@dataclass
class Patient:
    id: str
    age: int
    gender: str
    symptoms: list[Symptom]=field(default_factory=list)
    test: list[Test]=field(default_factory=list)