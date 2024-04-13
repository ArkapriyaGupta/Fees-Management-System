from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask
from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin
from werkzeug.security import gen_salt, generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import random, string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secrets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy()

class User(UserMixin,db.Model):
    id = db.Column(db.String(1000), primary_key=True) # primary keys are required by SQLAlchemy
    mobile = db.Column(db.Integer)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
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
    