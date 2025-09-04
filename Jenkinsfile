pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/BethelemMelese/ai-cicd-pipeline.git',
                    credentialsId: 'github-creds'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python -m venv venv
                . venv/script/activate
                pip install --upgrade pip
                pip install -r /requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Build stage (placeholder)'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy stage (placeholder)'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
        success {
            echo 'All stages succeeded'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
