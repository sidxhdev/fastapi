pipeline {
    agent any
    environment {
        AWS_REGION = 'ap-south-1'
        S3_BUCKET  = 'fastapi-inventory-frontend'
        EC2_IP     = '43.205.124.153'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/sidxhdev/fastapi'
            }
        }
        stage('Run Backend') {
            steps {
                withCredentials([
                    string(credentialsId: 'DATABASE_URL', variable: 'DATABASE_URL')
                ]) {
                    sh '''
                        echo "DATABASE_URL=$DATABASE_URL" > .env
                        docker stop fastapi-backend || true
                        docker rm fastapi-backend || true
                        docker compose down || true
                        docker compose up -d --build
                    '''
                }
            }
        }
        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh '''
                        echo "REACT_APP_API_URL=https://api.inventory-manager.sidxh.com" > .env.production
                        npm install
                        npm run build
                    '''
                }
            }
        }
        stage('Deploy Frontend to S3') {
            steps {
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                        aws s3 sync frontend/build/ s3://$S3_BUCKET/ \
                            --region $AWS_REGION \
                            --delete
                    '''
                }
            }
        }
    }
    post {
        success {
            echo "Live at: http://$S3_BUCKET.s3-website.$AWS_REGION.amazonaws.com"
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}