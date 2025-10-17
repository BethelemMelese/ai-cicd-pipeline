# ai/ai_test_selector.py
import pandas as pd
import joblib
import os
import argparse

MODEL = "data/model.pkl"
PROCESSED = "data/processed_dataset.csv"
OUT = "selected_tests.txt"

def select_tests(model_path=MODEL, processed_path=PROCESSED, out_path=OUT, top_k=None, prob_threshold=None):
    # Load processed dataset (this should represent known tests in repo)
    df = pd.read_csv(processed_path)
    feature_cols = ['past_runs','failures','avg_duration_s','code_change_size','failure_rate','flakiness','failure_x_duration']
    X = df[feature_cols].fillna(0)
    # Load model
    model = joblib.load(model_path)
    probs = model.predict_proba(X)[:,1]  # probability of failure
    df = df.copy()
    df['fail_prob'] = probs
    # Option A: choose top_k tests
    if top_k is not None:
        sel = df.sort_values('fail_prob', ascending=False).head(top_k)
    elif prob_threshold is not None:
        sel = df[df['fail_prob'] >= prob_threshold].sort_values('fail_prob', ascending=False)
    else:
        # fallback: choose tests with prob above mean
        sel = df[df['fail_prob'] >= df['fail_prob'].mean()].sort_values('fail_prob', ascending=False)
    tests = sel['test_nodeid'].tolist()
    # write to file
    with open(out_path, "w") as fh:
        for t in tests:
            fh.write(t + "\n")
    print(f"Selected {len(tests)} tests. Wrote to {out_path}")
    return tests

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--top_k", type=int, default=None)
    parser.add_argument("--prob_threshold", type=float, default=None)
    args = parser.parse_args()
    os.makedirs(".", exist_ok=True)
    select_tests(top_k=args.top_k, prob_threshold=args.prob_threshold)
