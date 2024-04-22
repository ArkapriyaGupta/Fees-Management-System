from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask
from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin
from werkzeug.security import gen_salt, generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import random, string,utilities
from utilities import genAlphaNum

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secrets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy()


class Student(UserMixin,db.Model):
    token = db.Column(db.Integer(), primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    password = db.Column(db.String(1000))
    mobile = db.Column(db.String(1000)) 
    userName = db.Column(db.String(1000))

class Teacher(UserMixin,db.Model):
    token = db.Column(db.Integer(), primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    password = db.Column(db.String(1000))
    mobile = db.Column(db.String(1000)) 
    userName = db.Column(db.String(1000))

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

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup',methods=['POST'])
#request.form.get(<name of the tag>)
def signupPost():
    #Taking input from browser
    try:
        Name = request.form.get('nameName')
        passWord =  generate_password_hash(request.form.get('passwordName'),method='pbkdf2:sha256')
        mobileNumber = request.form.get('mobileName')
        username = request.form.get("username")
        roleValue=request.form.get('roleName')
    except: 
        return render_template('error.html',error_message=utilities.errorList['inputError'])
 
    #Saving student input
    
    if roleValue == 'Student':  #Check for dupicacy
        try:
            student= Student.query.filter_by(userName=username).first()
            if student:
                return render_template('error.html', error_message=utilities.errorList['duplicateUser'])
        except:
            return render_template('error.html', error_message=utilities.errorList['generalError'])

        if(Name!=None and passWord!=None and mobileNumber != None):    
            newStudent = Student(name=Name,password=passWord,mobile=mobileNumber,userName=username)
            db.session.add(newStudent)
            db.session.commit()
        else:
            return render_template('error.html',error_message=utilities.errorList['emptyInput'])
        
    #Saving teacher input 
    elif roleValue == 'Teacher':    #Check for duplicacy 
        try:
            teacher= teacher.query.filter_by(userName=username).first()
            if student:
                return render_template('error.html', error_message=utilities.errorList['duplicateUser'])
        except:
            return render_template('error.html', error_message=utilities.errorList['generalError'])

        if(Name!=None and passWord!=None and mobileNumber != None):    
            newTeacher= Teacher(name=Name,password=passWord,mobile=mobileNumber,userName=username)
            db.session.add(newTeacher)
            db.session.commit()
        else:
            return render_template('error.html',error_message=utilities.errorList['emptyInput'])
    else:
        return render_template('error.html',error_message=utilities.errorList['invalidRole'])

    return redirect(url_for('signupStudent'))


# 

if __name__ == "__main__":
    app.run(debug=True) 
