# ai/feature_engineering.py
import pandas as pd
import os

RAW = "data/raw_test_history.csv"
PROCESSED = "data/processed_dataset.csv"

def load_and_process(raw_path=RAW):
    df = pd.read_csv(raw_path)
    # Basic features:
    # - failure_rate = failures / past_runs
    df['failure_rate'] = df['failures'] / (df['past_runs'] + 1e-6)
    # - normalized duration (we'll keep raw)
    df['avg_duration_s'] = df['avg_duration_s']
    # - code_change_size as-is
    df['code_change_size'] = df['code_change_size']
    # - flakiness proxy: failures > 0 and low past_runs (example)
    df['flakiness'] = ((df['failures'] > 0) & (df['past_runs'] < 30)).astype(int)
    # optional: create interactions
    df['failure_x_duration'] = df['failure_rate'] * df['avg_duration_s']
    # Keep label
    if 'failed_next' not in df.columns:
        raise ValueError("raw file must include 'failed_next' label for supervised training")
    df.to_csv(PROCESSED, index=False)
    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = load_and_process()
    print("Processed dataset shape:", df.shape)
    print("Saved to", PROCESSED)
