import pandas as pd
from Logic.Default_Logic.Helpers import analyze_with_default_logic


def main():
    df = pd.read_csv("data/lung_cancer.csv")

    print("=" * 60)
    print("REITER DEFAULT LOGIC - LUNG CANCER RISK ANALYSIS")
    print("=" * 60)

    results = analyze_with_default_logic(df)

    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    accuracy = (correct / total) * 100 if total > 0 else 0

    print(f"Total Patients: {total}")
    print(f"Correct Predictions: {correct}")
    print(f"Accuracy: {accuracy:.2f}%\n")

    print("Sample Results:")
    print("-" * 80)
    print("ID | Predicted | Actual | Correct | Rules Applied")
    print("-" * 80)

    for r in results[:10]:
        rules = ", ".join(r["applied_rules"]) if r["applied_rules"] else "None"
        status = "Yes" if r["correct"] else "No"

        print(
            f"{r['patient_id']} | "
            f"{r['predicted'].value} | "
            f"{r['actual'].value if r['actual'] else 'Unknown'} | "
            f"{status} | "
            f"{rules}"
        )


if __name__ == "__main__":
    main()
