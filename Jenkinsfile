pipeline {
    agent any
    stages{
        stage('Cloning the repo') {
            steps{
                git branch: 'main', changelog: false, poll: false, url: 'https://github.com/x091204/Two-Tier-Flask-App-DevOps-Project.git'
            }
        }
        stage('Build docker image') {
            steps{
                sh 'docker build -t two-tier-app:latest .'
            }
        }
        stage('Deploy') {
            steps{
                sh 'docker compose down -v || true'
                sh 'docker compose up -d --build'
            }
        }
    }
}