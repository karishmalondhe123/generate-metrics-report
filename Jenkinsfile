pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/karishmalondhe123/generate-metrics-report.git'  // Replace with your repository URL
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ec2-metrics-report .'
            }
        }

        stage('Run Report Generation') {
            steps {
                sh 'docker run --rm -v $WORKSPACE/reports:/app/reports ec2-metrics-report'
            }
        }

        stage('Archive Report') {
            steps {
                archiveArtifacts artifacts: 'reports/*.xlsx', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo 'Report generated and archived successfully.'
        }
        cleanup {
            sh 'docker system prune -f'
        }
    }
}
