pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Set Environment Variables') {
            steps {
                bat 'set APP_NAME=PTA'
                bat 'set SERVICE_NAME=REQRES'
                bat 'set REGION=QA'
                bat 'set BROWSER=CHROME'
                bat 'set HEADLESS=N'
            }
        }
        stage('Install Python Dependencies') {
            steps {
                bat 'pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Run Pytest') {
            steps {
                bat 'pytest -vvv -m "pta or reqres" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 --html=output/reports/report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'output/reports/report.html', allowEmptyArchive: true
            archiveArtifacts artifacts: 'output/allure-results/**', allowEmptyArchive: true
        }
    }
}
