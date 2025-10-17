# data_prep/defects4j_extractor.py
import os
import csv
import subprocess
import json

OUT_CSV = "data/defects4j_tests.csv"
# list of project IDs in defects4j (e.g., Chart, Lang, Math, Time)
PROJECTS = ["Chart", "Lang", "Math", "Time"]  # pick subset to limit time

def run(cmd, cwd=None):
    print("RUN:", cmd)
    r = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        print("ERR:", r.stderr[:400])
    return r.stdout

def process():
    os.makedirs("data", exist_ok=True)
    rows = []
    for pr in PROJECTS:
        # get number of bugs for project
        stdout = run(f"defects4j query -p {pr} -q \"id\"", cwd=None)
        ids = [line.strip() for line in stdout.splitlines() if line.strip()]
        for bid in ids:
            # checkout buggy version
            run(f"defects4j checkout -p {pr} -v {bid}b -w work/{pr}_{bid} ", cwd=None)
            # run tests and capture failing testcases
            run(f"defects4j test -w work/{pr}_{bid}", cwd=None)
            # get test results
            out = run(f"defects4j info -w work/{pr}_{bid} -r", cwd=None)
            # Note: parse relevant parts; for demo we will mark whole revision has failing tests and collect the failing test names
            # Use defects4j command to list failing tests or examine reports in work/{pr}_{bid}/target
            # This pseudocode assumes you parse and extract test nodeids and durations if available
            # Append rows like: project,bid,test_nodeid,fail_next,execution_time,code_change_size,...
            # You will need Java/junit parsing to get durations (or run tests with a timer)
    # write CSV (after you parsed)
    with open(OUT_CSV, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["project","bug_id","test_nodeid","failed","duration_s","code_change_size"])
        # write rows...
    print("Saved", OUT_CSV)

if __name__ == "__main__":
    process()
