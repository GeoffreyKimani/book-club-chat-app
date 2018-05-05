from flask import request, render_template, flash, url_for
from werkzeug.utils import redirect

from chat_app.config import *


@app.route('/login', methods=['POST', 'GET'])
def login_user():
    page_title = 'Login'
    # on request to do a login
    if request.method == 'GET':
        return render_template('login.html', page_title=page_title)

    # on request to submit login form
    elif request.method == 'POST':

        # connect to the database
        connection = mysql.connect()
        cursor = connection.cursor()

        # fetch user name and format it to be displayed in the index page when logged in
        cursor.execute('SELECT user_name FROM users WHERE user_email = (%s)',
                       request.form['email'])

        username = str(cursor.fetchone())
        unwanted_char = ["'", "(", ")", ", "]
        for i in range(len(unwanted_char)):
            username = username.replace(unwanted_char[i], " ")
        print(username)

        # dictonary of values to check
        kwargs = {
            'email': request.form['email'],
            'password': request.form['password'],
            'secret_key': request.form['secret_key'],
            'username': username
        }

        # check if a user with the given email exits, if they don't take them to signup
        check_user_exists = cursor.execute('SELECT user_email FROM users WHERE user_email = (%s)',
                                           request.form['email'])
        print("There exists " + str(check_user_exists) + " with this email:" + request.form['email'])
        if check_user_exists == 0:
            flash('Sorry User does not exist! Visit ')
            return render_template('login.html', page_title=page_title)

        # if user exists log them in
        elif check_user_exists > 0:
            cursor.execute('SELECT user_email, user_password FROM users WHERE user_email = (%s)',
                           request.form['email'])
            if 'user_password' == request.form['password']:
                print('success')
            else:
                flash('Incorrect Password')

            return render_template('index.html', username=kwargs)
        else:
            print('some errors')
        cursor.close()
        print('cursor closed')
        connection.close()
        print('connection closed')


# redirect a user who has no account
@app.route('/signup')
def try_signup():
    from chat_app.sign_up import create_user
    return create_user()


from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        print('database adding user')
        flash('Thanks for registering')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/home')
def index():
    return render_template('index.html')
