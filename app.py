import os
from dotenv import load_dotenv

from flask_bootstrap import Bootstrap
from flask_gravatar import Gravatar
from flask_login import LoginManager

from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from forms.forms import LoginForm, Registerform
from models.users import User

from db import db


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('secret_key')

Bootstrap(app) # integrates with Bootstrap css
Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None ) # Allows for generation of gravatar url i.le associates avatar images with email address
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('database_url')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False
app.config["PROPAGATE_EXCEPTIONS"] = True
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Registerform()
    if form.validate_on_submit():
        # check if user exist already and redirect them to login instead
        email = form.email.data
        user = User.find_by_email(email=email)
        if user:
            flash('User already exist')
            return redirect(url_for('login'))
        # if not hash and salt the password and create new user
        password = form.password.data
        confirmed_password = form.confirm_password.data
        if password != confirmed_password:
            flash('Passwords do not match. Please try again')
            return(redirect(url_for('register')))
        hashed_password = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )

        # create the user
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            mobile_number=form.mobile_number.data,
            email=form.email.data,
            password=hashed_password
        )
        # save user to db
        user.add_user()
        flash('registration successful! Please log in to continue.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.find_by_email(email=email)
        if not user: # user does not exists but tries to login
            flash('That email does not exist, Please try again.')
            return redirect(url_for('login'))
        ## Check if user exist but password is not correct
        elif not check_password_hash(user.password, password=password):
            flash('Incorrect Password, pleas try again')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form, current_user=current_user)

@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    user = User.find_by_userid(user_id=user_id)
    if user:
        user_details = {
            'first_name': user.first_name,
            'last_name' : user.last_name
        }

        product_details = {

        }

        transaction_details = {

        }
        return render_template('dashboard.html', user=user_details, products=product_details, transaction=transaction_details)
    
    return render_template('error.html') # define an endpoint to display error page


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)

