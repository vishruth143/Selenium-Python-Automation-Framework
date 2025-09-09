// Jenkins Pipeline for Selenium-Python-Automation-Framework
// This pipeline builds a Docker image, runs tests inside a container, copies results, and archives reports.
pipeline {
    agent any // Run on any available Jenkins agent
    parameters {
        // Select browser for test execution
        choice(name: 'BROWSER', choices: ['CHROME', 'FIREFOX', 'EDGE'], description: 'Browser to run tests on')
    }
    environment {
        // Set environment variables for the test run
        APP_NAME = 'PTA'
        MOBILE_APP_NAME = 'KWA'
        SERVICE_NAME = 'REQRES'
        REGION = 'qa'
        HEADLESS = 'Y'
        DOCKER_IMAGE = 'selenium-python-automation' // Docker image name
        OUTPUT_CONTAINER = 'selenium_test_container' // Container name for test run
    }
    stages {
        stage('Checkout') {
            steps {
                // Checkout source code from SCM
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                // Build Docker image from Dockerfile in workspace
                bat 'docker build -t %DOCKER_IMAGE% .'
            }
        }
        stage('Run Tests in Docker') {
            steps {
                // Remove any previous container with the same name
                bat 'docker rm -f %OUTPUT_CONTAINER% 2>nul'
                // Set BROWSER environment variable from Jenkins parameter
                bat 'set BROWSER=%BROWSER%'
                // Run tests inside Docker container, passing environment variables
                // Note: Use %BROWSER% to pass the correct value, not ${params.BROWSER}
                bat 'docker run --name %OUTPUT_CONTAINER% -e APP_NAME=%APP_NAME% -e SERVICE_NAME=%SERVICE_NAME% -e REGION=%REGION% -e BROWSER=%BROWSER% -e HEADLESS=%HEADLESS% %DOCKER_IMAGE% pytest -vvv -m "pta or reqres" -n 4 --maxfail=1 --log-cli-level=INFO --reruns 3 --html=output/reports/report.html --alluredir=output/allure-results --self-contained-html --capture=tee-sys --durations=10 tests'
            }
        }
        stage('Copy Results from Container') {
            steps {
                // Copy output directory (reports, logs, screenshots) from container to Jenkins workspace
                bat 'docker cp %OUTPUT_CONTAINER%:/app/output %WORKSPACE%'
            }
        }
        stage('Cleanup Container') {
            steps {
                // Remove the test container after copying results
                bat 'docker rm -f %OUTPUT_CONTAINER% 2>nul'
            }
        }
    }
    post {
        always {
            // Archive HTML and Allure reports for Jenkins job
            archiveArtifacts artifacts: 'output/reports/report.html', allowEmptyArchive: true
            archiveArtifacts artifacts: 'output/allure-results/**', allowEmptyArchive: true
        }
    }
}
