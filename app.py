import os
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Config — use env vars, never hardcode
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'mysql')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'DevOps@123')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'student_db')

mysql = MySQL(app)

# Home page - view students
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', students=data)

# Add student page
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        grade = request.form['grade']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO students(name, roll_no, grade) VALUES(%s,%s,%s)",
            (name, roll, grade)
        )
        mysql.connection.commit()
        cur.close()
        return redirect('/')

    return render_template('add_student.html')  # ✅ Moved here

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')  # ✅ Dead code removed

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)