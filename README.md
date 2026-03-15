# Two-Tier Flask App — DevOps Project

web app built with **Flask + MySQL**, containerised with Docker and deployed on **AWS EC2** with a Jenkins CI/CD pipeline.

---

## 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Flask](https://img.shields.io/badge/Flask-lightgrey)
![MySQL](https://img.shields.io/badge/MySQL-orange)
![Docker](https://img.shields.io/badge/Docker-blue)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-red)
![AWS](https://img.shields.io/badge/AWS-EC2-yellow)

---

## 📌 What This Project Does

- Add, view, and delete student records via a Flask web interface
- MySQL database with persistent Docker volume
- Multi-container setup with Docker Compose and custom networking
- MySQL health check ensures Flask only starts when the DB is ready
- Jenkins pipeline automates build and deployment on every push

---

## ⚙️ CI/CD Pipeline

```
Clone Repo → Build Docker Image → Deploy with Docker Compose
```

---

## 🏗 Architecture

```
Developer → GitHub → Jenkins (EC2)
                          |
              +-----------+-----------+
              |                       |
       Flask Container          MySQL Container
       (two-tier-app)              (mysql)
              |                       |
              +-----------+-----------+
                          |
                    two-tier-net
                  (Docker Network)
```

---

## 📁 Project Structure

```
├── db/
│   └── init.sql
├── templates/
│   ├── index.html
│   └── add_student.html
├── static/
│   └── style.css
├── app.py
├── config.py
├── Dockerfile
├── docker-compose.yml
└── Jenkinsfile
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/x091204/Two-Tier-Flask-App-DevOps-Project.git
cd Two-Tier-Flask-App-DevOps-Project
docker compose up -d --build
```

App runs at `http://localhost:5000`
