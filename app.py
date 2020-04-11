from flask import Flask, render_template, redirect, url_for, request, session
from wtforms.fields.html5 import EmailField
from wtforms.fields import PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length, ValidationError
from flask_wtf import FlaskForm
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import random

app = Flask(__name__)
app.secret_key = 'secret_key'

bcrypt = Bcrypt(app)

client = MongoClient('mongodb+srv://Winkel:test@cluster0-s5yjd.mongodb.net/test?retryWrites=true&w=majority')
db = client.get_database('food_story')
usersCollection = db.get_collection('users')
reservationsCollection = db.get_collection('reservations')

# Custom validator to check if email already exists
def email_exists(form, field):
    if (usersCollection.count_documents({'email': field.data}, limit=1) != 0):
        raise ValidationError('Email is already in use')

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), InputRequired(), email_exists])
    password = PasswordField('Password', validators=[Length(min=6, message='Password must have at least 6 characters'), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Register')

# Custom validator to check credentials on login
def incorrect_credentials(form, field):
    user = usersCollection.find_one({'email':field.data})
    if (user == None or not bcrypt.check_password_hash(user['password'],form.password.data)):
        raise ValidationError('Incorrect Credentials')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), InputRequired(), incorrect_credentials])
    password = PasswordField('Password')
    submit = SubmitField('Login')

@app.route('/')
def mainpage():
    return render_template('homepage.html')

@app.route('/content')
def content():
    return render_template('content.html')

@app.route('/bibimbap')
def bibimbap():
    return render_template('food/bibimbap.html')

@app.route('/pho')
def pho():
    return render_template('food/pho.html')

@app.route('/shawarma')
def shawarma():
    return render_template('food/shawarma.html')

@app.route('/sushi')
def sushi():
    return render_template('food/sushi.html')

@app.route('/surprise')
def surprise():
    links = ['bibimbap', 'pho', 'shawarma', 'sushi']
    index = random.randint(0, len(links)-1)
    return redirect(url_for(links[index]))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        account = {
            "email": form.email.data.strip(),
            "password": bcrypt.generate_password_hash(form.password.data.strip())
        }
        usersCollection.insert_one(account)
        session['email'] = form.email.data.strip()
        return "Welcome " + session.get('email')
    return render_template('auth/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data.strip()
        return redirect(url_for('mainpage'))
    return render_template('auth/login.html', form=form)

@app.route('/signout')
def signout():
    session.pop('email')
    return redirect(url_for('mainpage'))

@app.route('/random')
def random():
    return session.get('email', 'No email')

if __name__ == '__main__':
    app.run()
