pipeline {
    agent any
    // environment {
        // Define AWS credentials file environment variable
      //  AWS_SHARED_CREDENTIALS_FILE = '/var/lib/jenkins/.aws/credentials'
    //} 

    stages {
        stage('Clone Repository') {
            steps {
                // Cloning the master/main branch (make sure to specify the correct branch name)
                git branch: 'main', url: 'https://github.com/karishmalondhe123/generate-metrics-report.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the Docker image
                sh 'docker build -t ec2-metrics-report .'
            }
        }

        stage('Run Report Generation') {
            steps {
                // Run the Docker container, mounting the .aws directory and reports directory
                sh 'docker run --rm -v $JENKINS_HOME/.aws:/root/.aws -v $WORKSPACE/reports:/app/reports ec2-metrics-report'
            }
        }

        stage('Archive Report') {
            steps {
                // Archive the generated report
                archiveArtifacts artifacts: 'reports/*.xlsx', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo 'Report generated and archived successfully.'
        }
        cleanup {
            // Clean up unused Docker resources
            sh 'docker system prune -f'
        }
    }
}
