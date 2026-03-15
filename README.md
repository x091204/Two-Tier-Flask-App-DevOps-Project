# Student Record System (Flask + MySQL)

A simple web application built with **Python Flask and MySQL** that allows users to manage student records.
This project was created as a **practice application for DevOps workflows**, including containerization, CI/CD pipelines, and security scanning.

---

## Features

* Add new student records
* View all students in a table
* Delete student records
* Simple web interface using HTML and CSS
* MySQL database integration

---

## Tech Stack

* **Backend:** Python (Flask)
* **Database:** MySQL
* **Frontend:** HTML, CSS
* **Version Control:** Git & GitHub

---

## Project Structure

```
student-record-system
│
├── app.py
├── config.py
├── requirements.txt
│
├── templates
│   ├── index.html
│   └── add_student.html
│
├── static
│   └── style.css
│
└── db
    └── init.sql
```

---

## Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/yourusername/student-record-system.git
cd student-record-system
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Setup MySQL Database

Login to MySQL:

```
mysql -u root -p
```

Create database:

```
CREATE DATABASE student_db;
```

Run the SQL initialization file:

```
mysql -u root -p student_db < db/init.sql
```

---

### 4. Configure Database Connection

Update `config.py` with your MySQL credentials:

```
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "yourpassword"
MYSQL_DB = "student_db"
```

---

### 5. Run the Application

```
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Future DevOps Enhancements

This project will be extended with:

* Docker containerization
* Jenkins CI/CD pipeline
---

## Purpose of the Project

This application is used as a **practice project for learning DevOps tools and workflows**, including automation, containerization, and deployment strategies.

---

## Author
akifmuhammed
