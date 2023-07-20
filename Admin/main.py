from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json


with open('config.json','r') as c:
    params=json.load(c)["params"]

local_server=True


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,


)


mail=Mail(app)
if(local_server):
     app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    grade = db.Column(db.String(10))

    def __init__(self,id, name, age, grade):
        self.id = id
        self.name = name
        self.age = age
        self.grade = grade
class login_info_student(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(80))
    def __init__(self,username,password):
        self.username = username
        self.password = password




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Add your authentication logic here
        # For simplicity, we'll assume admin/admin as the login credentials
        if username == 'admin' and password == 'admin':
            return redirect('/dashboard')

    return render_template('login.html')


@app.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Add your authentication logic here
        # For simplicity, we'll assume admin/admin as the login credentials

        if username == 'student' and password == 'student':
            return redirect('/student_dashboard')

    return render_template('studentlogin.html')

@app.route('/student_dashboard')
def stu_dashboard():
    student = Student.query.all()


    return render_template('student_dashboard.html', params=params,student=student)

@app.route('/dashboard')
def dashboard():
    student = Student.query.all()
    return render_template('dashboard.html', params=params,student=student)


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        id=int(request.form['id'])
        name = request.form['name']
        age = int(request.form['age'])
        grade = request.form['grade']

        student = Student(id=id,name=name, age=age, grade=grade)
        db.session.add(student)
        db.session.commit()

        return redirect('/dashboard')

    return render_template('add.html',params=params)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get(id)

    if request.method == 'POST':
        student.id = int(request.form['id'])
        student.name = request.form['name']
        student.age = int(request.form['age'])
        student.grade = request.form['grade']

        db.session.commit()
        return redirect('/dashboard')

    return render_template('edit.html', params=params,student=student)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    student = Student.query.get(id)

    if request.method == 'POST':
        db.session.delete(student)
        db.session.commit()
        return redirect('/dashboard')

    return render_template('delete.html', student=student,params=params)



app.run(debug=True)
