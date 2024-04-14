from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask
from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin
from werkzeug.security import gen_salt, generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import random, string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secrets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy()

errorList = {}
errorList["generalError"] = "Sorry! We ran into an error. Please try again."
errorList["duplicateUser"] = "Sorry! the user already exist. Please login."
errorList["saveError"] = "Some error occured in saving the data. Please try again."
errorList["inputError"] = "Could not fetch input. Please try again."
errorList["emptyInput"] = "One of the input field is empty. Please try again"

class Student(UserMixin,db.Model):
    studentId = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    password = db.Column(db.String(1000))
    mobile = db.Column(db.String(1000))    
    # role = db.Column(db.String(1000))

db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Student.query.get(user_id)


@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/signupStudent')
def signupStudent():
    return render_template('signup.html')

@app.route('/signupStudent',methods=['POST'])
#request.form.get(<name of the tag>)
def signupStudentPost():
    try:
        studentName = request.form.get('nameName')
        passWord =  generate_password_hash(request.form.get('passwordName'),method='pbkdf2:sha256')
        mobileNumber = request.form.get('mobileName')
        # roleValue=Markup.escape(request.form.get('roleName'))
    except: 
        return render_template('error.html',error_message=errorList['inputError'])
    
    # try:
    #     student= Student.query.filter_by(name=studentName).first()
    # except: 
    #     return render_template('error.html',error_message=errorList['generalError'])
        
    # if student:
    #     return render_template('error.html',error_message=errorList['duplicateUser'])

    if(studentName!=None and passWord!=None and mobileNumber != None):    
        newStudent = Student(name=studentName,password=passWord,mobile=mobileNumber)
        db.session.add(newStudent)
        db.session.commit()
    else:
        return render_template('error.html',error_message=errorList['emptyInput'])
    
    return redirect(url_for('signupStudent'))




if __name__ == "__main__":
    app.run(debug=True) 
