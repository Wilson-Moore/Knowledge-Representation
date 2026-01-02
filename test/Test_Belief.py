import pandas as pd
from collections import Counter
from Logic.Belief_Functions.Helpers import analyze_with_belief


def main():
    df = pd.read_csv("data/lung_cancer.csv")

    print("=" * 60)
    print("HIERARCHICAL DEMPSTER–SHAFER ANALYSIS")
    print("=" * 60)

    results = analyze_with_belief(df)

    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    accuracy = (correct / total * 100) if total else 0.0

    print(f"\nTotal patients: {total}")
    print(f"Correct predictions: {correct}")
    print(f"Accuracy: {accuracy:.2f}%")

    dist = Counter(r["predicted"].value for r in results)
    print("\nPrediction distribution:")
    for k, v in dist.items():
        print(f"  {k}: {v}")

    print("\nSample predictions:")
    for r in results[:5]:
        print(
            f"Pred={r['predicted'].value} | "
            f"Actual={r['actual'].value if r['actual'] else 'Unknown'} | "
            f"Conf={r['confidence']:.3f}"
        )


if __name__ == "__main__":
    main()