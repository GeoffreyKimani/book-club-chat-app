import requests
from wtforms import Form, StringField, validators, PasswordField
from flask import Blueprint, render_template, redirect, url_for, request, flash, session

login_bp = Blueprint('login_bp', __name__, static_folder='static', template_folder='templates')


# log-in form
class LogInForm(Form):
    email = StringField("Email Address", [validators.Email()])
    password = PasswordField("Password", [validators.InputRequired()])


@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    page_title = "Log In"
    form = LogInForm(request.form)
    session.pop('user', None)

    if request.method == 'POST' and form.validate():
        # connect to the database
        from ChatApp import mysql
        connection = mysql.connect()
        cursor = connection.cursor()

        # fetch user name and format it to be displayed in the index page when logged in
        cursor.execute('SELECT username FROM user WHERE email = (%s)',
                       request.form['email'])

        username = str(cursor.fetchone())
        formatted_username = format_db_string(username)

        # dictonary of values to check
        kwargs = {
            'email': request.form['email'],
            'password': request.form['password'],
            'secret_key': request.form['secret_key'],
            'username': formatted_username
        }

        # check if a user with the given email exits, if they don't take them to signup
        check_user_exists = cursor.execute('SELECT email FROM user WHERE email = (%s)',
                                           request.form['email'])

        from ChatApp import app
        if check_user_exists == 0:
            flash('Sorry User does not exist! Visit ')
            app.logger.info('***********Unknown user ' + str(request.form['email']) + ' trying to log '
                                                                                      'in...*************')
            return render_template('login.html', form=form, page_title=page_title)

        # if user exists create a session then log them in
        elif check_user_exists > 0:
            app.logger.info("There exists " + str(check_user_exists) + " user(s) with this email: " +
                            request.form['email'])
            if cursor.execute('SELECT password FROM user WHERE email = (%s)',
                              request.form['email']):
                user_password = format_db_string(str(cursor.fetchone()))
                print(user_password)

                from ChatApp import bcrypt
                hashed_checker = bcrypt.check_password_hash(user_password, request.form['password'])
                print(hashed_checker)

                # on successful login add a session
                if hashed_checker:
                    session['user_id'] = request.form['email']
                    session['user'] = formatted_username.upper()
                    app.logger.info('Successful Login by user ' + str(formatted_username) +
                                    ' of email ' + str(session['user_id']) + " on session of " + str(
                        session['user']))

                    cursor.execute('SELECT book_club_id FROM admin WHERE email = (%s)', request.form['email'])
                    admin = cursor.fetchone()
                    if admin:
                        session['admin'] = request.form['email']
                        app.logger.info('user ' + str(formatted_username) + 'is admin of book club ' + str(admin))

                    cursor.close()
                    connection.close()
                    app.logger.info('cursor and connection closed...')

                    return redirect(url_for('chatter_bp.show_posts'))
                else:
                    form.password.errors = ["Incorrect Password!"]
                    app.logger.info("User Input Incorrect Password!!! ")
                    return render_template('login.html', form=form, page_title=page_title)

            return app.logger.info('Nothing was selected from the database...')

        else:
            app.logger.error('Some error occurred')

        cursor.close()
        connection.close()
        app.logger.info('cursor and connection closed...')

    return render_template('login.html', form=form, page_title=page_title)


# UDFs
def format_db_string(db_string):
    unwanted_char = ["'", "(", ")", ","]
    for i in range(len(unwanted_char)):
        db_string = db_string.replace(unwanted_char[i], "")
    return db_string


@login_bp.route('/red_signup')
def try_signup():
    return redirect(url_for("login_bp.login"))
