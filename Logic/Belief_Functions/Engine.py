from typing import Dict
from Knowledge.Hierarchy import RiskLevel


class BeliefEngine:
    """
    Calibrated belief-based inference engine
    (Dempster–Shafer inspired, but decision-oriented)
    """

    def _norm(self, v):
        """Normalize symptom severity to [0,1]"""
        try:
            return min(max(float(v) / 10.0, 0.0), 1.0)
        except Exception:
            return 0.0

    def infer(self, row) -> Dict:

        # --- Normalize symptoms (UI-safe: missing => 0) ---
        blood = self._norm(row.get("Coughing of Blood", 0))
        weight = self._norm(row.get("Weight Loss", 0))
        breath = self._norm(row.get("Shortness of Breath", 0))
        air = self._norm(row.get("Air Pollution", 0))
        alcohol = self._norm(row.get("Alcohol use", 0))

        chest = self._norm(row.get("Chest Pain", 0))
        fatigue = self._norm(row.get("Fatigue", 0))
        cough = self._norm(row.get("Dry Cough", 0))
        wheeze = self._norm(row.get("Wheezing", 0))

        cold = self._norm(row.get("Frequent Cold", 0))
        snore = self._norm(row.get("Snoring", 0))

        smoking = self._norm(row.get("Smoking", 0))
        passive = self._norm(row.get("Passive Smoker", 0))

        # Evidence construction

        # LOW risk: weak / common symptoms
        low_evidence = (
            cold * 0.4 +
            snore * 0.4 +
            air * 0.3 +
            fatigue * 0.3 
        )

        # MEDIUM risk: functional impairment
        medium_evidence = (
            chest * 0.4 +
            cough * 0.4 +
            weight * 0.3 +
            breath * 0.2 +
            alcohol * 0.2
        )

        # HIGH raw evidence
        high_raw = (
            blood * 1.2 +
            smoking * 0.6 +
            wheeze * 0.7
        )

        # Severity gating (CRITICAL)
        strong_high = max(blood, weight, breath)

        if strong_high < 0.5:
            high_evidence = high_raw * 0.4
        else:
            high_evidence = high_raw

        # Competition (belief interaction)
        high_evidence *= (1 - 0.5 * medium_evidence)
        medium_evidence *= (1 - 0.3 * low_evidence)

        # Dataset priors (calibration)
        priors = {
            RiskLevel.LOW: 0.35,
            RiskLevel.MEDIUM: 0.35,
            RiskLevel.HIGH: 0.30,
        }

        beliefs = {
            RiskLevel.LOW: low_evidence * priors[RiskLevel.LOW],
            RiskLevel.MEDIUM: medium_evidence * priors[RiskLevel.MEDIUM],
            RiskLevel.HIGH: high_evidence * priors[RiskLevel.HIGH],
        }

        # Normalize
        total = sum(beliefs.values())

        if total == 0:
            beliefs = {
                RiskLevel.LOW: 0.33,
                RiskLevel.MEDIUM: 0.33,
                RiskLevel.HIGH: 0.34,
            }
        else:
            beliefs = {k: v / total for k, v in beliefs.items()}

        predicted = max(beliefs, key=beliefs.get)

        return {
            "predicted": predicted,
            "beliefs": beliefs,
            "confidence": beliefs[predicted]
        }
