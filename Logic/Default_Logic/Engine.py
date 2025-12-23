from Knowledge.Hierarchy import RiskLevel

class DefaultRule:
    def __init__(self, name, prerequisite, justification, conclusion):
        self.name = name
        self.prerequisite = prerequisite
        self.justification = justification
        self.conclusion = conclusion


class ReiterDefaultEngine:
    """
    Simple implementation of Reiter's Default Logic.
    Applies default rules based on known facts about a patient.
    """

    def __init__(self, rules):
        self.rules = rules

    def evaluate(self, patient):
        facts = self._extract_facts(patient)

        applied_rules = []
        final_risk = RiskLevel.LOW

        for rule in self.rules:
            if rule.prerequisite in facts:
                if self._is_consistent(rule.justification, facts):
                    applied_rules.append(rule.name)

                    if self._risk_value(rule.conclusion) > self._risk_value(final_risk):
                        final_risk = rule.conclusion

        return {
            "patient_id": patient.id,
            "predicted": final_risk,
            "applied_rules": applied_rules,
            "method": "Reiter Default Logic"
        }

    def _extract_facts(self, patient):
        facts = {}

        for symptom in patient.symptoms:
            facts[symptom.name] = symptom.severity

        facts["age"] = patient.age

        if patient.age > 50:
            facts["is_senior"] = True

        if facts.get("smoking_history", 0) >= 7:
            facts["heavy_smoker"] = True

        if facts.get("coughing_of_blood", 0) >= 5:
            facts["severe_symptom"] = True

        if facts.get("air_pollution_exposure", 0) >= 6:
            facts["high_pollution"] = True

        return facts

    def _is_consistent(self, justification, facts):
        if justification == "HighRisk":
            if facts.get("age", 0) < 25 and facts.get("smoking_history", 0) == 0:
                return False
        return True

    def _risk_value(self, risk):
        if risk == RiskLevel.LOW:
            return 1
        if risk == RiskLevel.MEDIUM:
            return 2
        if risk == RiskLevel.HIGH:
            return 3
        return 0
