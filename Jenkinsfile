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
                        def tests = readFile('selected_tests.txt').trim().split("\\r?\\n")
                        for (t in tests) {
                            sh "pytest -k ${t}"
                        }
                    } else {
                        sh "pytest"
                    }
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

