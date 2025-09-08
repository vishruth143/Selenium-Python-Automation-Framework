pipeline {
    agent any

    environment {
        APP_NAME = 'PTA'
        SERVICE_NAME = 'REQRES'
        REGION = 'qa'
        BROWSER = 'CHROME'
        HEADLESS = 'Y'
        PYTHON_VERSION = '3.13.3'
        IMAGE_NAME = 'selenium-python-automation'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Run Tests in Docker') {
            steps {
                bat "docker run --rm -v %cd%/output:/app/output %IMAGE_NAME% pytest -vvv -m \"pta or reqres\" -n 4 --reruns 3 --html=output/reports/pta_report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests"
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat '''
                if not exist "C:\\allure\\bin\\allure.bat" (
                    powershell -Command "Invoke-WebRequest -Uri https://github.com/allure-framework/allure2/releases/download/2.34.1/allure-2.34.1.zip -OutFile allure.zip"
                    powershell -Command "Expand-Archive -Path allure.zip -DestinationPath C:\\allure"
                    setx PATH "%PATH%;C:\\allure\\bin"
                )
                allure generate output/allure-results --clean -o output/allure-report
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'output/**', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'output/**', allowEmptyArchive: true
        }
    }
}
