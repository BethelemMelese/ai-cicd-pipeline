// pipeline {
//     agent {
//         docker {
//             image 'python:3.12'
//             args '-u root:root'   // run as root inside container so pip installs work
//         }
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Install dependencies') {
//             steps {
//                 sh 'pip install --no-cache-dir -r requirements.txt'
//             }
//         }
//         stage('AI Test Selector') {
//             steps {
//                 sh 'python ai_test_selector.py'
//             }
//         }
//         stage('Run Tests') {
//             steps {
//                 sh 'pytest --maxfail=1 --disable-warnings -q'
//             }
//         }

//         stage('Build') {
//             steps {
//                 echo 'Build step (later we can package app or build Docker image)'
//             }
//         }

//         stage('Deploy') {
//             steps {
//                 echo 'Deploy step (later we can push to Docker Hub or staging)'
//             }
//         }
//     }

//     post {
//         always {
//             echo 'Pipeline finished!'
//         }
//         success {
//             echo 'Pipeline succeeded!'
//         }
//         failure {
//             echo 'Pipeline failed!'
//         }
//     }
// }

pipeline {
    agent {
        docker { image 'python:3.12' }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install dependencies') {
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }
        stage('AI Test Selector') {
            steps {
                sh 'python ai_test_selector.py'
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    if (fileExists('selected_tests.txt')) {
                        sh 'pytest $(cat selected_tests.txt) --junitxml=results.xml'
                    } else {
                        sh 'pytest --junitxml=results.xml'
                    }
                }
            }
        }

        stage('Update History') {
            steps {
                script {
                    // Parse pytest results and update history
                    sh '''
                    python - <<'EOF'
                    import xml.etree.ElementTree as ET
                    import pandas as pd
                    import os

                    history_file = "data/test_history.csv"
                    results_file = "results.xml"

                    # Load existing history
                    if os.path.exists(history_file):
                        df = pd.read_csv(history_file)
                    else:
                        df = pd.DataFrame(columns=["test_nodeid","past_runs","failures","avg_duration_s"])

                    # Parse JUnit XML
                    tree = ET.parse(results_file)
                    root = tree.getroot()

                    for testcase in root.iter("testcase"):
                        nodeid = f"{testcase.get('classname')}::{testcase.get('name')}"
                        duration = float(testcase.get('time', 0))
                        failed = testcase.find("failure") is not None

                        if nodeid in df["test_nodeid"].values:
                            row = df.loc[df["test_nodeid"] == nodeid]
                            df.loc[df["test_nodeid"] == nodeid, "past_runs"] = int(row["past_runs"]) + 1
                            df.loc[df["test_nodeid"] == nodeid, "failures"] = int(row["failures"]) + (1 if failed else 0)
                            # update running average
                            old_avg = float(row["avg_duration_s"])
                            runs = int(row["past_runs"])
                            new_avg = (old_avg * (runs - 1) + duration) / runs
                            df.loc[df["test_nodeid"] == nodeid, "avg_duration_s"] = new_avg
                        else:
                            df = pd.concat([df, pd.DataFrame([{
                                "test_nodeid": nodeid,
                                "past_runs": 1,
                                "failures": 1 if failed else 0,
                                "avg_duration_s": duration
                            }])])

                    df.to_csv(history_file, index=False)
                    EOF
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                echo "Building application..."
            }
        }
        stage('Deploy') {
            steps {
                echo "Deploying application..."
            }
        }
    }
}

