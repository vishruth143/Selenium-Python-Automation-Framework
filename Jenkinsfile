pipeline {
    agent any
    parameters {
        choice(name: 'BROWSER', choices: ['CHROME', 'FIREFOX', 'EDGE'], description: 'Browser to run tests on')
    }
    environment {
        APP_NAME = 'PTA'
        SERVICE_NAME = 'REQRES'
        REGION = 'qa'
        HEADLESS = 'Y'
        DOCKER_IMAGE = 'selenium-python-automation'
        OUTPUT_DIR = "${env.WORKSPACE}/output"
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
                bat 'if not exist output mkdir output'
                bat 'docker run --rm -e APP_NAME=%APP_NAME% -e SERVICE_NAME=%SERVICE_NAME% -e REGION=%REGION% -e BROWSER=%BROWSER% -e HEADLESS=%HEADLESS% -v %OUTPUT_DIR%:/app/output %DOCKER_IMAGE% pytest -vvv -m "pta or reqres" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 --html=output/reports/report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests'
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
