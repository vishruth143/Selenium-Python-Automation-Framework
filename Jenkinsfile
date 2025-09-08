pipeline {
    agent any
    parameters {
        choice(name: 'BROWSER', choices: ['CHROME', 'FIREFOX', 'EDGE'], description: 'Browser to run tests on')
    }
    environment {
        APP_NAME = 'PTA'
        SERVICE_NAME = 'REQRES'
        REGION = 'qa'
        BROWSER = 'CHROME'
        HEADLESS = 'Y'
        DOCKER_IMAGE = 'selenium-python-automation'
        OUTPUT_CONTAINER = 'selenium_test_container'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %DOCKER_IMAGE% .'
            }
        }
        stage('Run Tests in Docker') {
            steps {
                bat 'docker rm -f %OUTPUT_CONTAINER% 2>nul'
                bat 'docker run --name %OUTPUT_CONTAINER% -e APP_NAME=%APP_NAME% -e SERVICE_NAME=%SERVICE_NAME% -e REGION=%REGION% -e BROWSER=%BROWSER% -e HEADLESS=%HEADLESS% %DOCKER_IMAGE% pytest -vvv -m "pta or reqres" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 --html=output/reports/report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests'
            }
        }
        stage('Copy Results from Container') {
            steps {
                bat 'docker cp %OUTPUT_CONTAINER%:/app/output %WORKSPACE%'
            }
        }
        stage('Cleanup Container') {
            steps {
                bat 'docker rm -f %OUTPUT_CONTAINER% 2>nul'
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
