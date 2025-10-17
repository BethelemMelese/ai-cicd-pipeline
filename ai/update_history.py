# ai/update_history.py
import xml.etree.ElementTree as ET
import pandas as pd
import os
import csv

RAW = "data/raw_test_history.csv"
RESULTS = "results.xml"

def append_results(results_xml=RESULTS, raw_csv=RAW):
    if not os.path.exists(results_xml):
        print("No results.xml found.")
        return
    tree = ET.parse(results_xml)
    root = tree.getroot()
    # JUnit XML structure: testsuite/testcase with failure children
    rows = []
    for testcase in root.iter('testcase'):
        name = testcase.get('classname') + "::" + testcase.get('name') if testcase.get('classname') else testcase.get('name')
        # if junit xml uses 'classname' differently, you may need to adapt
        failures = 1 if testcase.find('failure') is not None else 0
        # Set placeholders for past_runs / avg_duration / code_change_size
        rows.append({
            "test_nodeid": name,
            "past_runs": 1,
            "failures": failures,
            "avg_duration_s": 0.05,
            "code_change_size": 0,
            "failed_next": failures
        })
    # Append rows to CSV
    os.makedirs(os.path.dirname(raw_csv), exist_ok=True)
    exists = os.path.exists(raw_csv)
    with open(raw_csv, "a", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["test_nodeid","past_runs","failures","avg_duration_s","code_change_size","failed_next"])
        if not exists:
            writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"Appended {len(rows)} results to {raw_csv}")

if __name__ == "__main__":
    append_results()
