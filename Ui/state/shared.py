class PatientState:
    def __init__(self):
        self.age = None
        self.gender = None
        self.symptoms = []
        self.method = None

    def reset(self):
        self.age = None
        self.gender = None
        self.symptoms = []
        self.method = None

patient_state = PatientState()

patient_data = {
    "age": None,
    "gender": None,
    "symptoms": [],
    "method": None
}
