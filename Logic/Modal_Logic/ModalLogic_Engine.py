from dataclasses import dataclass

@dataclass
class ModalLogic:
    
    def necessary(self,patient,propositions):
            return all(proposition.fn(patient) for proposition in propositions)
    def possible(self,patient,propositions):
            return any(proposition.fn(patient) for proposition in propositions)