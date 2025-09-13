import pandas as pd
import os

def select_tests():
    history_file = "test_history.csv"
    output_file = "selected_tests.txt"

    if not os.path.exists(history_file):
        print(":: No test history found, running all tests.")
        return

    try:
        df = pd.read_csv(history_file)

        # prioritize tests that failed more than once
        failed_tests = df[df['status'] == 'fail']['test_name'].unique()

        if len(failed_tests) > 0:
            print(":: Selected failed tests for rerun:", failed_tests)
            with open(output_file, "w") as f:
                for test in failed_tests:
                    f.write(test + "\n")
        else:
            print(":: No failed tests, running all tests")
    except Exception as e:
        print(":: Error in test selection:", e)

if __name__ == "__main__":
    select_tests()
