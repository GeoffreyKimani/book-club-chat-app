from wtforms import Form, StringField, validators, PasswordField
from flask import Blueprint, render_template, redirect, url_for, request, flash

login_bp = Blueprint('login_bp', __name__, static_folder='static', template_folder='templates')


# log-in form
class LogInForm(Form):
    email = StringField("Email Address", [validators.Email()])
    password = PasswordField("Password", [validators.InputRequired()])


@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    page_title = "Log In"
    form = LogInForm(request.form)

    if request.method == 'POST' and form.validate():
        # connect to the database
        from ChatApp import mysql
        connection = mysql.connect()
        cursor = connection.cursor()

        # fetch user name and format it to be displayed in the index page when logged in
        cursor.execute('SELECT user_name FROM users WHERE user_email = (%s)',
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
        check_user_exists = cursor.execute('SELECT user_email FROM users WHERE user_email = (%s)',
                                           request.form['email'])

        from ChatApp import app
        if check_user_exists == 0:
            flash('Sorry User does not exist! Visit ')
            app.logger.info('***********Unknown user ' + str(request.form['email']) + 'trying to log '
                                                                                      'in...*************')
            return render_template('login.html', form=form, page_title=page_title)

        # if user exists log them in
        elif check_user_exists > 0:
            app.logger.info("There exists " + str(check_user_exists) + " with this email: " + request.form['email'])
            if cursor.execute('SELECT user_password FROM users WHERE user_email = (%s)',
                              request.form['email']):
                user_password = str(cursor.fetchone())
                formatted_user_password = format_db_string(user_password)

                if formatted_user_password == request.form['password']:
                    app.logger.info('Successful Login by user ' + str(formatted_username) +
                                    ' of email ' + str(request.form['email']))
                    return redirect(url_for('chatter_bp.show_posts', username=formatted_username))
                else:
                    password_error = "Incorrect Password!"
                    app.logger.info("User Input Incorrect Password!!! ")
                    return render_template('login.html', form=form, password_error=password_error, page_title=page_title)

            app.logger.info('Nothing was selected from the database...')

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


