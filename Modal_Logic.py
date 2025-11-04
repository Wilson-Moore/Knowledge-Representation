from dataclasses import dataclass

@dataclass
class Modal_Logic:

    def necessary(self,conditions):
        return all(conditions)
    
    def possible(self,conditions):
        return any(conditions)