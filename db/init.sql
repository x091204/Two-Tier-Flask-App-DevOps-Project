from flask import Flask
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "mysql")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "DevOps@123")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "student_db")

mysql = MySQL(app)