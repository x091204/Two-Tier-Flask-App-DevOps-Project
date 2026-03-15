# Two-Tier-Flask-App-DevOps-Project (Flask + MySQL)

---

### **Table of Contents**
1. [Project Overview](#1-project-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [Step 1: AWS EC2 Instance Preparation](#3-step-1-aws-ec2-instance-preparation)
4. [Step 2: Install Dependencies on EC2](#4-step-2-install-dependencies-on-ec2)
5. [Step 3: Jenkins Installation and Setup](#5-step-3-jenkins-installation-and-setup)
6. [Step 4: GitHub Repository Configuration](#6-step-4-github-repository-configuration)
    * [Dockerfile](#dockerfile)
    * [docker-compose.yml](#docker-composeyml)
    * [Jenkinsfile](#jenkinsfile)
    * [tests/test_app.py](#teststest_apppy)
7. [Step 5: Jenkins Pipeline Creation and Execution](#7-step-5-jenkins-pipeline-creation-and-execution)
8. [Conclusion](#8-conclusion)

---

### **1. Project Overview**
This document outlines the step-by-step process for deploying a 2-tier web application (Flask + MySQL) on an AWS EC2 instance. The application is a student records management system that allows users to add, view, and delete student entries. The deployment is containerised using Docker and Docker Compose. A full CI/CD pipeline is established using Jenkins to automate the build, test, security scan, and deployment process whenever new code is pushed to the GitHub repository.

---

### **2. Architecture Diagram**

```
+-----------------+      +----------------------+      +-----------------------------+
|   Developer     |----->|     GitHub Repo      |----->|        Jenkins Server       |
| (pushes code)   |      | (Source Code Mgmt)   |      |  (on AWS EC2)               |
+-----------------+      +----------------------+      |                             |
                                                       | 1. Clones Repo              |
                                                       | 2. Runs Pytest Tests        |
                                                       | 3. Builds Docker Image      |
                                                       | 4. Trivy Security Scan      |
                                                       | 5. Runs Docker Compose      |
                                                       +--------------+--------------+
                                                                      |
                                                                      | Deploys
                                                                      v
                                                       +-----------------------------+
                                                       |      Application Server     |
                                                       |      (Same AWS EC2)         |
                                                       |                             |
                                                       | +-------------------------+ |
                                                       | | Docker Container: Flask | |
                                                       | | (two-tier-app)          | |
                                                       | +-------------------------+ |
                                                       |              |              |
                                                       |              v              |
                                                       | +-------------------------+ |
                                                       | | Docker Container: MySQL | |
                                                       | | (mysql)                 | |
                                                       | +-------------------------+ |
                                                       +-----------------------------+
```

---

### **3. Step 1: AWS EC2 Instance Preparation**

1. **Launch EC2 Instance:**
    * Navigate to the AWS EC2 console.
    * Launch a new instance using the **Ubuntu 22.04 LTS** AMI.
    * Select the **t2.micro** instance type (free-tier eligible).
    * Create and assign a new key pair for SSH access.

2. **Configure Security Group:**
    * Create a security group with the following inbound rules:
        * **Type:** SSH, **Protocol:** TCP, **Port:** 22, **Source:** Your IP
        * **Type:** Custom TCP, **Protocol:** TCP, **Port:** 5000 (Flask), **Source:** Anywhere (0.0.0.0/0)
        * **Type:** Custom TCP, **Protocol:** TCP, **Port:** 8080 (Jenkins), **Source:** Anywhere (0.0.0.0/0)
        * **Type:** Custom TCP, **Protocol:** TCP, **Port:** 3306 (MySQL), **Source:** Your IP only

3. **Connect to EC2 Instance:**
    ```bash
    ssh -i /path/to/key.pem ubuntu@<ec2-public-ip>
    ```

---

### **4. Step 2: Install Dependencies on EC2**

1. **Update System Packages:**
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

2. **Install Git, Docker, and Docker Compose:**
    ```bash
    sudo apt install git docker.io docker-compose-v2 -y
    ```

3. **Start and Enable Docker:**
    ```bash
    sudo systemctl start docker
    sudo systemctl enable docker
    ```

4. **Add User to Docker Group:**
    ```bash
    sudo usermod -aG docker $USER
    newgrp docker
    ```

5. **Install Python and Pytest (for pipeline test stage):**
    ```bash
    sudo apt install python3-pip -y
    pip install pytest pytest-flask --break-system-packages
    ```

---

### **5. Step 3: Jenkins Installation and Setup**

1. **Install Java (OpenJDK 17):**
    ```bash
    sudo apt install openjdk-17-jdk -y
    ```

2. **Add Jenkins Repository and Install:**
    ```bash
    curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
    echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
    sudo apt update
    sudo apt install jenkins -y
    ```

3. **Start and Enable Jenkins:**
    ```bash
    sudo systemctl start jenkins
    sudo systemctl enable jenkins
    ```

4. **Initial Jenkins Setup:**
    * Retrieve the initial admin password:
        ```bash
        sudo cat /var/lib/jenkins/secrets/initialAdminPassword
        ```
    * Access Jenkins at `http://<ec2-public-ip>:8080`
    * Paste the password, install suggested plugins, and create an admin user.

5. **Grant Jenkins Docker Permissions:**
    ```bash
    sudo usermod -aG docker jenkins
    sudo systemctl restart jenkins
    ```

---

### **6. Step 4: GitHub Repository Configuration**

Ensure your GitHub repository contains the following files.

#### **Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl gcc default-libmysqlclient-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

#### **docker-compose.yml**
```yaml
version: '3.8'
services:
  db:
    container_name: mysql
    image: mysql
    environment:
      MYSQL_DATABASE: student_db
      MYSQL_ROOT_PASSWORD: DevOps@123
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - two-tier-net
    restart: always
    healthcheck:
      test: ["CMD", "mysqladmin","ping","-h","localhost","-uroot","-pDevOps@123"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 60s

  flask:
    build:
      context: .
    container_name: two-tier-app
    ports:
      - "5000:5000"
    environment:
      - MYSQL_HOST=db
      - MYSQL_USER=root
      - MYSQL_PASSWORD=DevOps@123
      - MYSQL_DB=student_db
    networks:
      - two-tier-net
    depends_on:
      db:
        condition: service_healthy
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:5000/health || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 60s

volumes:
  mysql-data:

networks:
  two-tier-net:
```

> **Note:** `MYSQL_HOST` must be set to `db` (the service name), not `localhost`. Flask connects to MySQL over the Docker network, not via a local socket.

#### **Jenkinsfile**
```groovy
pipeline {
    agent any
    stages {
        stage('Cloning the repo') {
            steps {
                git branch: 'main', changelog: false, poll: false,
                    url: 'https://github.com/x091204/Two-Tier-Flask-App-DevOps-Project.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt --break-system-packages'
                sh 'pip install pytest pytest-flask --break-system-packages'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest tests/ -v --tb=short'
            }
            post {
                failure { echo 'Tests failed — pipeline stopped' }
                success { echo 'All tests passed' }
            }
        }
        stage('Build docker image') {
            steps {
                sh 'docker build -t two-tier-app:latest .'
            }
        }
        stage('Trivy Security Scan') {
            steps {
                sh '''
                    if ! command -v trivy &> /dev/null; then
                        curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
                    fi
                    trivy image --exit-code 1 --severity CRITICAL --no-progress two-tier-app:latest
                '''
            }
            post {
                failure { echo 'CRITICAL vulnerabilities found — pipeline stopped' }
                success { echo 'No CRITICAL vulnerabilities found' }
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker compose down -v || true'
                sh 'docker compose up -d --build'
            }
        }
    }
}
```

#### **tests/test_app.py**
```python
import pytest, sys, os
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    with patch('app.mysql') as mock_mysql:
        mock_mysql.connection.cursor.return_value = MagicMock()
        mock_mysql.connection.cursor().fetchall.return_value = []
        response = client.get('/')
        assert response.status_code == 200

def test_add_student_get(client):
    response = client.get('/add')
    assert response.status_code == 200

def test_add_student_post(client):
    with patch('app.mysql') as mock_mysql:
        mock_mysql.connection.cursor.return_value = MagicMock()
        response = client.post('/add', data={'name': 'Arjun', 'roll': 'RS101', 'grade': 'A'})
        assert response.status_code == 302

def test_delete_student(client):
    with patch('app.mysql') as mock_mysql:
        mock_mysql.connection.cursor.return_value = MagicMock()
        response = client.get('/delete/1')
        assert response.status_code == 302

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
```

---

### **7. Step 5: Jenkins Pipeline Creation and Execution**

1. **Create a New Pipeline Job:**
    * From the Jenkins dashboard, click **New Item**.
    * Name the project, select **Pipeline**, and click **OK**.

2. **Configure the Pipeline:**
    * Scroll to the **Pipeline** section.
    * Set **Definition** to **Pipeline script from SCM**.
    * Choose **Git** as the SCM.
    * Enter your GitHub repository URL.
    * Set the branch to `*/main`.
    * Verify **Script Path** is set to `Jenkinsfile`.
    * Save the configuration.

3. **Run the Pipeline:**
    * Click **Build Now** to trigger the first run.
    * Monitor progress via **Stage View** or **Console Output**.
    * The pipeline will run: Clone → Install → Test → Build → Trivy Scan → Deploy.

4. **Verify Deployment:**
    * After a successful build, the app is accessible at `http://<your-ec2-public-ip>:5000`.
    * Confirm containers are running:
        ```bash
        docker ps
        ```

---

### **8. Conclusion**

The CI/CD pipeline is now fully operational. Any `git push` to the `main` branch will automatically trigger Jenkins to install dependencies, run Pytest unit tests, build the Docker image, scan it for vulnerabilities with Trivy, and deploy the full stack using Docker Compose — ensuring a fully automated workflow from development to production on AWS EC2.
