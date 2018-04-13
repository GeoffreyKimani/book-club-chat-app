"""This is the signup code. I first created the fuction create_user() to have the logic of the sign up process, however later learnt of wtForms that make validation easier and thus
created another function 'signup()' to try the form out. i have however run into some problems. the form wont validate even when the input is correct. solutions given are to include
a csrf_token which i have done but nothing has changed. please check out the code to see any anomalies. """
from flask import request, render_template, flash, url_for
from werkzeug.utils import redirect

from chat_app.config import *
from chat_app.log_in import login_user


@app.route('/signup', methods=['POST', 'GET'])
def create_user():
    page_title = 'Signup'
    if request.method == 'GET':
        return render_template('signup.html', page_title=page_title)
    elif request.method == 'POST':
        kwargs = {
            'email': request.form['email'],
            'username': request.form['username'],
            'password': request.form['password'],
            'secret_key': request.form['secret_key']
        }
        connection = mysql.connect()
        cursor = connection.cursor()
        check_user_exists = cursor.execute('SELECT user_email FROM users WHERE user_email = (%s)',
                                           request.form['email'])
        print("There exists " + str(check_user_exists) + " users with this email:" + request.form['email'])

        if check_user_exists > 0:
            flash('Sorry user already exists! Try a different email, or try')
            return render_template('signup.html', page_title=page_title)
        else:
            cursor.execute('INSERT INTO users (user_email, user_name, user_password) VALUES (%s,%s,%s)',
                           (request.form['email'], request.form['username'], request.form['password']))
            connection.commit()
            return render_template('index.html', **kwargs)


@app.route('/login')
def try_login():
    return login_user


from wtforms import StringField, Form, validators, PasswordField, BooleanField
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
csrf.init_app(app)


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])


@app.route('/sign_up', methods=['POST', 'GET'])
def signup():
    form = RegistrationForm(request.form)
    page_title = 'Signup'

    if request.method == 'POST' and form.validate():
        print('database adding user')
        print('posting, validation complete')
        flash('Thanks for registering')
        return redirect(url_for('indexs'))

    for field, errors in form.errors.items():
        print("error field: " + str(field) + " Actual error: " + str(errors))

    print("serving get request")
    return render_template('signup.html', form=form)


@app.route('/home')
def indexs():
    return render_template('index.html')
