# ai/generate_dataset.py
import csv
import random
import os

os.makedirs("data", exist_ok=True)
OUT = "data/raw_test_history.csv"

tests = [
    "tests/test_add.py::test_add_basic",
    "tests/test_add.py::test_add_negative",
    "tests/test_add.py::test_add_large_numbers",
    "tests/test_subtract.py::test_subtract_basic",
    "tests/test_subtract.py::test_subtract_negative",
    "tests/test_subtract.py::test_subtract_large_numbers",
    "tests/test_multiply.py::test_multiply_basic",
    "tests/test_multiply.py::test_multiply_by_zero",
    "tests/test_multiply.py::test_multiply_large_numbers",
    "tests/test_divide.py::test_divide_basic",
    "tests/test_divide.py::test_divide_fraction",
    "tests/test_divide.py::test_divide_by_zero"
]

# We'll generate many historical runs for each test to simulate richer history
rows = []
for t in tests:
    past_runs = random.randint(20, 200)
    # failures roughly correlated with test difficulty
    failures = max(0, int(random.gauss(0.2 * past_runs, 3)))
    avg_duration_s = round(random.uniform(0.03, 0.5), 3)
    # create multiple sample rows per test to emulate time series (optional)
    rows.append({
        "test_nodeid": t,
        "past_runs": past_runs,
        "failures": failures,
        "avg_duration_s": avg_duration_s,
        # label: whether test failed on the *next run* (0/1). We'll generate probabilistically
        "failed_next": 1 if random.random() < (failures / (past_runs + 1)) else 0,
        # a synthetic code change size in lines
        "code_change_size": random.randint(0, 200)
    })

# To simulate 200+ rows, duplicate with small variation
expanded = []
for r in rows:
    for i in range(random.randint(5, 20)):
        pr = max(1, r["past_runs"] + random.randint(-3, 3))
        f = max(0, r["failures"] + random.randint(-2, 2))
        dd = max(0.01, round(r["avg_duration_s"] + random.uniform(-0.02, 0.02), 3))
        failed_next = 1 if random.random() < (f / (pr + 1)) else 0
        cs = max(0, r["code_change_size"] + random.randint(-10, 10))
        expanded.append({
            "test_nodeid": r["test_nodeid"],
            "past_runs": pr,
            "failures": f,
            "avg_duration_s": dd,
            "code_change_size": cs,
            "failed_next": failed_next
        })

# Save CSV
with open(OUT, "w", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=["test_nodeid","past_runs","failures","avg_duration_s","code_change_size","failed_next"])
    writer.writeheader()
    for r in expanded:
        writer.writerow(r)

print(f"Wrote {len(expanded)} rows to {OUT}")
