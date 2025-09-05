pipeline {
    agent any

    environment {
        APP_NAME = 'PTA'
        SERVICE_NAME = 'REQRES'
        REGION = 'qa'
        BROWSER = 'CHROME'
        HEADLESS = 'Y'
        PYTHON_VERSION = '3.13.3'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Install ffmpeg') {
            steps {
                bat '''
                if not exist "C:\ffmpeg\bin\ffmpeg.exe" (
                    powershell -Command "Invoke-WebRequest -Uri https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z -OutFile ffmpeg.7z"
                    powershell -Command "Expand-7ZipArchive -Path ffmpeg.7z -DestinationPath C:\ffmpeg"
                    setx PATH "%PATH%;C:\ffmpeg\bin"
                )
                ffmpeg -version
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                pytest -vvv -m "pta or reqres" ^
                  -n 4 ^
                  --reruns 3 ^
                  --html=output/reports/pta_report.html ^
                  --alluredir=output/allure-results ^
                  --self-contained-html ^
                  --capture=tee-sys ^
                  --durations=10 ^
                  tests
                '''
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
