# scripts/generate_combined_dataset.py
import numpy as np
import pandas as pd
import random, os

random.seed(42)
np.random.seed(42)

N = 200  # sample size (you can change to 100/300)
projects = ['projA','projB','projC']
tests_per_project = 80

rows = []
for i in range(N):
    proj = random.choice(projects)
    test_file = f"tests/{proj}/test_module_{random.randint(1,tests_per_project)}.py"
    test_func = f"::test_func_{random.randint(1,50)}"
    test_nodeid = test_file + test_func

    past_runs = np.random.randint(20,201)
    code_change_size = np.random.randint(0,201)
    base_failure_prob = 0.05 + (code_change_size / 400.0)
    failures = np.random.binomial(past_runs, min(base_failure_prob + np.random.rand()*0.05, 0.9))
    avg_duration_s = float(max(0.01, np.random.normal(0.05 + failures*0.002 + code_change_size*0.0005, 0.02)))
    failure_rate = failures / past_runs if past_runs > 0 else 0.0
    flakiness = float(min(0.5, np.random.beta(1+max(0,failures), 5) + np.random.rand()*0.05))

    # Scoring function that correlates features with a next-failure probability
    score = 0.4*failure_rate + 0.3*(code_change_size/200.0) + 0.2*flakiness + np.random.normal(0,0.05)
    failed_next = 1 if score > 0.25 else 0

    rows.append({
        "test_nodeid": test_nodeid,
        "project": proj,
        "past_runs": int(past_runs),
        "failures": int(failures),
        "avg_duration_s": round(avg_duration_s, 3),
        "code_change_size": int(code_change_size),
        "failed_next": int(failed_next),
        "failure_rate": round(failure_rate,3),
        "flakiness": round(flakiness,3)
    })

df = pd.DataFrame(rows)

# If the classes are very imbalanced, duplicate minority (simple balancing)
counts = df['failed_next'].value_counts()
if counts.min() / counts.max() < 0.8:
    needed = int(counts.max() - counts.min())
    samples = df[df['failed_next']==counts.idxmin()]
    to_add = samples.sample(needed, replace=True, random_state=42).copy()
    # small jitter to numeric columns
    for col in ['past_runs','failures','avg_duration_s','code_change_size','failure_rate','flakiness']:
        if col in to_add.columns:
            jitter = np.random.normal(0, 0.01, size=len(to_add))
            if col in ['past_runs','failures','code_change_size']:
                to_add[col] = (to_add[col].astype(float) * (1 + jitter)).round().clip(1).astype(int)
            else:
                to_add[col] = (to_add[col].astype(float) * (1 + jitter)).round(3).clip(0)
    df = pd.concat([df, to_add], ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)

# Save to data/combined_dataset.csv
os.makedirs('data', exist_ok=True)
csv_path = 'data/combined_dataset.csv'
df.to_csv(csv_path, index=False)
print(f"Saved dataset to {csv_path} (rows={len(df)})")
print(df[['test_nodeid','failed_next']].head(8).to_string(index=False))
