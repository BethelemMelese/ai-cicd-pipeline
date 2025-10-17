# ai/merge_datasets.py
import pandas as pd
import os

def merge(defects_csv="data/defects4j_tests.csv", pytest_csv="data/pytest_tests.csv", out="data/combined_dataset.csv"):
    # defects4j has labels in 'failed' with project and bug id
    df_d = pd.read_csv(defects_csv)
    # For Pytest, you need labeling: if you have historical runs or CI failure history, add 'failed' flag.
    df_p = pd.read_csv(pytest_csv)
    # For demo: convert pytest durations to synthetic history (if you don't have failures)
    # Create columns to match
    def normalize(df):
        df = df.copy()
        if 'past_runs' not in df.columns:
            df['past_runs'] = 50
        if 'failures' not in df.columns:
            df['failures'] = (df['test_nodeid'].apply(lambda x: 1 if 'fail' in x else 0)).astype(int)
        if 'avg_duration_s' not in df.columns and 'duration_s' in df.columns:
            df['avg_duration_s'] = df['duration_s']
        if 'code_change_size' not in df.columns:
            df['code_change_size'] = 10
        if 'failed' in df.columns:
            df['failed_next'] = df['failed']
        elif 'failed_next' not in df.columns:
            df['failed_next'] = (df['failures'] > 0).astype(int)
        return df[['test_nodeid','project','past_runs','failures','avg_duration_s','code_change_size','failed_next']]
    # adapt dataframe names
    if 'project' not in df_d.columns:
        df_d['project'] = 'defects4j'
    if 'project' not in df_p.columns:
        df_p['project'] = 'pytest'
    dfd = normalize(df_d)
    dfp = normalize(df_p)
    dfc = pd.concat([dfd, dfp], ignore_index=True)
    dfc['failure_rate'] = dfc['failures'] / (dfc['past_runs'] + 1e-6)
    dfc['flakiness'] = ((dfc['failures'] > 0) & (dfc['past_runs'] < 30)).astype(int)
    dfc.to_csv(out, index=False)
    print("Combined dataset saved to", out)

if __name__ == "__main__":
    merge()
