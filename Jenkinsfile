pipeline {
    agent {
        docker {
            image 'python:3.12'    // Python image to run inside
            args '-u root:root'    // run as root so pip installs work
        }
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

        stage('Run Tests') {
            steps {
                sh 'pytest --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Build') {
            steps {
                echo 'Build step placeholder (later can package app or build Docker image)'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy step placeholder (later can push to Docker Hub or deploy to staging)'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
