pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m py_compile app.py
                    python -m py_compile tests/test_app.py
                    flake8 app.py tests
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest -q
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t aceest-fitness:jenkins .
                '''
            }
        }
    }

    post {
        always {
            sh '''
                rm -rf .venv
            '''
        }

        success {
            echo 'ACEest Fitness Jenkins BUILD completed successfully.'
        }

        failure {
            echo 'ACEest Fitness Jenkins BUILD failed.'
        }
    }
}