import pandas as pd
from typing import List, Dict
from Knowledge.Hierarchy import RiskLevel
from Logic.Belief_Functions.Engine import BeliefEngine


def analyze_with_belief(df: pd.DataFrame, verbose: bool = False) -> List[Dict]:

    engine = BeliefEngine()
    results = []

    if verbose:
        print("Running Dempster–Shafer belief analysis...")

    for _, row in df.iterrows():
        inference = engine.infer(row)

        predicted = inference["predicted"]
        confidence = inference["confidence"]

        # Actual label (if exists)
        actual = None
        if "Level" in row:
            try:
                actual = RiskLevel(str(row["Level"]).strip().capitalize())
            except Exception:
                actual = None

        correct = predicted == actual if actual else False

        results.append({
            "patient_id": row.get("Patient Id", "UI"),
            "predicted": predicted,
            "predicted_risk": predicted,   # UI compatibility
            "actual": actual,
            "correct": correct,
            "belief": {k.value: v for k, v in inference["beliefs"].items()},
            "confidence": confidence
        })

        if verbose:
            print(
                f"Pred={predicted.value} | "
                f"Conf={confidence:.3f} | "
                f"Actual={actual.value if actual else 'N/A'}"
            )

    return results
