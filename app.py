import forms

from flask import Flask, render_template, redirect, request, flash, url_for
from email.policy import default
from enum import unique
from crypt import methods
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user



# create flask app
app = Flask(__name__)

# custom config file
app.config.from_pyfile("config.py")

# initialise the database
db = SQLAlchemy(app)

# create user model for database
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    data_added = db.Column(db.DateTime, default=datetime.utcnow)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/assets")
def assets():
    return render_template("assets.html")

@app.route("/liabilities")
def liabilities():
    return render_template("liabilities.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f"Hello {user.username}")
                return redirect("/")
            else:
                flash("Incorrect username and/or password")
        else:
            flash("Username does not exist")
    return render_template("login.html", form=form)

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("See you next time!")
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegistrationForm()

    if form.validate_on_submit():
        # check for duplicate usernames
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None:
            password_hash = generate_password_hash(form.password.data, method='sha256')
            user = Users(
                username=form.username.data, 
                password=password_hash)
            db.session.add(user)
            db.session.commit()

        else:
            flash("Username already exists")
            return render_template("register.html", form=form)
        login_user(user)
        flash(f"{user.username} has been registered succesfully!")
        return redirect("/")
    return render_template("register.html", form=form)
