# data_prep/pytest_extractor.py
import os, subprocess, csv

REPO_DIR = "pytest"
OUT_CSV = "data/pytest_tests.csv"

def run(cmd, cwd=None):
    print("RUN:", cmd)
    r = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        print("ERR:", r.stderr[:400])
    return r.stdout + r.stderr

def collect_test_durations(sample_pattern=None, max_tests=200):
    os.makedirs("data", exist_ok=True)
    # run pytest and produce junit xml
    if sample_pattern:
        cmd = f"pytest -q tests/ -k \"{sample_pattern}\" --junitxml=results.xml --durations=0 -q"
    else:
        cmd = f"pytest -q tests/ --junitxml=results.xml --durations=0 -q"
    out = run(cmd, cwd=REPO_DIR)
    # parse results.xml to get test nodeids and durations
    import xml.etree.ElementTree as ET
    tree = ET.parse(os.path.join(REPO_DIR, "results.xml"))
    root = tree.getroot()
    rows = []
    for testcase in root.iter('testcase'):
        classname = testcase.get('classname')
        name = testcase.get('name')
        # junit xml may not include exact duration attribute; sometimes it is in 'time'
        time = float(testcase.get('time') or 0.0)
        nodeid = f"{classname}::{name}" if classname else name
        rows.append((nodeid, time))
        if len(rows) >= max_tests:
            break
    with open(OUT_CSV, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["test_nodeid","duration_s"])
        writer.writerows(rows)
    print("Saved", OUT_CSV)

if __name__ == "__main__":
    collect_test_durations(sample_pattern=None, max_tests=300)
