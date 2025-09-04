import argparse
import pandas as pd
from pathlib import Path

"""
Simple AI-ish test prioritization:
- Reads historical test data from CSV with columns:
  test_nodeid, past_runs, failures, avg_duration_s
- Computes a simple risk score:
  risk = 0.7 * failure_rate + 0.3 * normalized_duration
- Outputs top-N tests (by fraction) to a file (one nodeid per line)
"""

def prioritize_tests(history_csv: Path, out_file: Path, top_fraction: float = 0.5):
    df = pd.read_csv(history_csv)
    # safety checks
    for col in ["test_nodeid", "past_runs", "failures", "avg_duration_s"]:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Compute failure rate
    df["failure_rate"] = (df["failures"] + 1) / (df["past_runs"] + 1)

    # Normalize duration to [0,1]
    dur = df["avg_duration_s"].astype(float)
    if dur.max() > dur.min():
        df["duration_norm"] = (dur - dur.min()) / (dur.max() - dur.min())
    else:
        df["duration_norm"] = 0.0

    # Risk score (tune weights as needed)
    df["risk_score"] = 0.7 * df["failure_rate"] + 0.3 * df["duration_norm"]

    # Sort by risk descending
    df = df.sort_values(by="risk_score", ascending=False)

    # Keep top fraction
    k = max(1, int(len(df) * top_fraction))
    top_df = df.head(k)

    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w") as f:
        for nodeid in top_df["test_nodeid"].tolist():
            f.write(f"{nodeid}\n")

    # Print a short report (visible in Jenkins logs)
    print("=== AI Prioritization Report ===")
    print(top_df[["test_nodeid", "failure_rate", "duration_norm", "risk_score"]])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--history", type=Path, required=True, help="Path to test_history.csv")
    parser.add_argument("--out", type=Path, required=True, help="Where to write prioritized test nodeids")
    parser.add_argument("--top", type=float, default=0.5, help="Fraction of tests to keep (0..1)")
    args = parser.parse_args()

    prioritize_tests(args.history, args.out, args.top)

if __name__ == "__main__":
    main()
