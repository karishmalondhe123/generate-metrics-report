pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                // Cloning the master/main branch (make sure to specify the correct branch name)
                git branch: 'main', url: 'https://github.com/karishmalondhe123/generate-metrics-report.git'
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
