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


class User(UserMixin,db.Model):
    id = db.Column(db.Integer(), primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    password = db.Column(db.String(1000))
    mobile = db.Column(db.String(1000)) 
    userName = db.Column(db.String(1000))
    role = db.Column(db.String(1000))

db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(user_id)


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
    
    #Check for dupicacy
    try:
        student= User.query.filter_by(userName=username).first()
        if student:
            return render_template('error.html', error_message=utilities.errorList['duplicateUser'])
    except:
            return render_template('error.html', error_message=utilities.errorList['generalError'])
    #Saving student input
      
    if(Name!=None and passWord!=None and mobileNumber != None):   
        try: 
            newUser = User(name=Name,password=passWord,mobile=mobileNumber,userName=username,role=roleValue)
            db.session.add(newUser)
            db.session.commit()
        except:
            return render_template('error.html', error_message=utilities.errorList['saveError'])
    else:
        return render_template('error.html',error_message=utilities.errorList['emptyInput'])
    
    return f"Signup successful for reole = {roleValue} "
    # return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def loginPost():
    #Taking input from browser
    try:
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('passwordName'),method='pbkdf2:sha256')
    except:
        return render_template('error.html', error_message=utilities.errorList['inputError'])

    #Check for duplicacy
    try:
        user= User.query.filter_by(userName=username).first()

        #Check for password match
        if user:
            if user.password == password:
                # login_user(user)
                login_user(user, remember=True)
                return render_template('homepage.html', user=user)
            else:
                #right username but wrong password
                return render_template('error.html', error_message=utilities.errorList['invalidPassword'])
        else:
            #wrong credentials
            return render_template('error.html', error_message=utilities.errorList['invalidUser'])
    except:
        ##for any error in validating
        return render_template('error.html', error_message=utilities.errorList['generalError'])
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('indexPage'))


if __name__ == "__main__":
    app.run(debug=True) 
