import forms
import itertools

from flask import Flask, render_template, redirect, request, flash, url_for
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

class Expenses(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    expense = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.String(100), nullable=False)


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
def dashboard():
    return render_template("dashboard.html")


@app.route("/assets")
def assets():
    return render_template("assets.html")


@app.route("/liabilities", methods=["GET", "POST"])
@login_required
def liabilities():

    # send data to database on submit
    if request.method == "POST":

        # select and delete all current records
        id = current_user.id
        Expenses.query.filter(Expenses.user_id == id).delete()
        db.session.commit()

        # get lists for each table column
        expenses = request.form.getlist("expense")
        amounts = request.form.getlist("amount")
        frequencies = request.form.getlist("frequency")

        # add each to database and include user_id in each row
        for (expense, amount, frequency) in zip(expenses, amounts, frequencies):
            user_id = current_user.id
            user_expenses = Expenses(
                user_id=user_id,
                expense=expense,
                amount=amount,
                frequency=frequency
            )
            db.session.add(user_expenses)
        
        # save changes to database
        db.session.commit()

        # return user to dashboard
        return redirect("/dashboard")
    
    # if request method = Get
    else:

        # check databse to see if user has already inputted expenses
        id = current_user.id
        query = Expenses.query.filter(Expenses.user_id == id).all()

        # if user has previous entries, return them to the HTML table
        if len(query) != 0:
            return render_template("liabilities.html", query=query)
        
        # if the user has no previous entries, display default
        elif len(query) == 0:

            frequency = [
                "Every Month",
                "Every 3 Months",
                "Every Week",
                "Every 2 Weeks"
            ]

            expenses = [
            "Mortgage/Rent",
            "Electricity",
            "Internet",
            "Other Utilities",
            "Car Payment",
            "Fuel",
            "Parking",
            "Insurance",
            "Car Tax",
            "Credit Card 1",
            "Credit Card 2",
            "Loan 1",
            "Loan 2",
            "Student Loan",
            "Netflix",
            "Spotify",
            "Gym"
        ]

            return render_template(
                "liabilities.html", 
                expenses=expenses,
                frequency=frequency
                )


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
        return redirect("/")
    return render_template("register.html", form=form)
