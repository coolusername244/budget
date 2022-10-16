import os
import forms
import itertools

from flask import Flask, render_template, redirect, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user



# create flask app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"

app.config["SECRET_KEY"] = os.urandom(24)

# initialise the database
db = SQLAlchemy(app)


# create user model for database
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    data_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Expenses(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    expense = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Income(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    income = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Savings(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    savings = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    
    id = current_user.id 
    income = 0
    outgoings = 0
    savings = 0

    query = Income.query.filter_by(user_id = id).all()
    for row in query:
        income += row.amount

    query = Expenses.query.filter_by(user_id = id).all()
    for row in query:
        outgoings += row.amount

    query = Savings.query.filter_by(user_id = id).all()
    for row in query:
        savings += row.amount

    remaining = income - outgoings - savings


    return render_template(
        "dashboard.html",
        income=income,
        savings=savings,
        outgoings=outgoings,
        remaining=remaining)


@app.route("/income", methods=["GET", "POST"])
@login_required
def income():

    incomes = [
        "Salary",
        "Dividends",
        "Rental Income",
        "Capital Gains",
        "Royalties"
        ]

    id = current_user.id 

    if request.method == "POST":
        # if user submits form, delete previous entries and 
        # update with current entries
        user_incomes = request.form.getlist("income")
        amounts = request.form.getlist("amount")
        Income.query.filter_by(user_id = id).delete()
        db.session.commit()
        if len(user_incomes) == 0:
            return render_template("income.html", incomes=incomes)
        for (income, amount) in zip(user_incomes, amounts):
            user_income = Income(
                user_id = id,
                income = income,
                amount = amount
            )
            db.session.add(user_income)
            db.session.commit()
        flash("Incomes Updated!")
        return redirect("/dashboard")
    else:
        # check if user has already completed the form and return
        # else provide default values
        query = Income.query.filter_by(user_id = id).all()
        if len(query) != 0:
            return render_template("income.html", query=query)
        else:
            return render_template("income.html", incomes=incomes)


@app.route("/outgoings", methods=["GET", "POST"])
@login_required
def outgoings():

    outgoings = [
                "Mortgage/Rent",
                "Home Insurance",
                "Car Payment",
                "Car Insurance",
                "Fuel",
                "Credit Card 1",
                "Credit Card 2",
                "Loan 1",
                "Loan 2",
                "Student Loan",
                "Netflix",
                "Spotify"
            ]

    id = current_user.id 

    if request.method == "POST":
        # if user submits form, delete previous entries and 
        # update with current entries
        expenses = request.form.getlist("expense")
        amounts = request.form.getlist("amount")
        Expenses.query.filter_by(user_id = id).delete()
        db.session.commit()
        if len(expenses) == 0:
            return render_template("outgoings.html", outgoings=outgoings)
        for (expense, amount) in zip(expenses, amounts):
            user_expense = Expenses(
                user_id = id,
                expense = expense,
                amount = amount
            )
            db.session.add(user_expense)
            db.session.commit()
        flash("Outgoings Updated!")
        return redirect("/dashboard")
    else:
        # check if user has already completed the form and return
        # else provide default values
        query = Expenses.query.filter_by(user_id = id).all()
        if len(query) != 0:
            return render_template("outgoings.html", query=query)
        else:
            return render_template("outgoings.html", outgoings=outgoings)


@app.route("/savings", methods=["GET", "POST"])
@login_required
def savings():

    savings = [
            "Emergency Fund",
            "Stock Portfolio",
            "Retirement Fund",
            "Commodites",
            "Other",
        ]

    id = current_user.id 

    if request.method == "POST":
        # if user submits form, delete previous entries and 
        # update with current entries
        user_savings = request.form.getlist("savings")
        amounts = request.form.getlist("amount")
        Savings.query.filter_by(user_id = id).delete()
        db.session.commit()
        if len(user_savings) == 0:
            return render_template("savings.html", savings=savings)
        for (saving, amount) in zip(user_savings, amounts):
            user_savings = Savings(
                user_id = id,
                savings = saving,
                amount = amount
            )
            db.session.add(user_savings)
            db.session.commit()
        flash("Savings Updated!")
        return redirect("/dashboard")
    else:
        # check if user has already completed the form and return
        # else provide default values
        query = Savings.query.filter_by(user_id = id).all()
        if len(query) != 0:
            return render_template("savings.html", query=query)
        else:
            return render_template("savings.html", savings=savings)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f"Hello {user.username}")
                return redirect("/dashboard")
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
        # if no duplicates found, create new user and add to db
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
        return redirect("/dashboard")
    return render_template("register.html", form=form)
