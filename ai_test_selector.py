import os
import pandas as pd

HISTORY_FILE = "data/test_history.csv"

def select_tests():
    if not os.path.exists(HISTORY_FILE):
        print(":: No test history found, running all tests.")
        return []

    df = pd.read_csv(HISTORY_FILE)
    failing_tests = df[df["failures"] > 0]["test_nodeid"].tolist()

    if failing_tests:
        print(f":: Selected failing tests from history: {failing_tests}")
        return failing_tests
    else:
        print(":: No failing tests found, running all tests.")
        return []

if __name__ == "__main__":
    selected = select_tests()
    if selected:
        # Write selected tests into a file so Jenkins can pick them up
        with open("selected_tests.txt", "w") as f:
            f.write("\n".join(selected))
