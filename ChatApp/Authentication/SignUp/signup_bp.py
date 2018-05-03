from wtforms import PasswordField, StringField, validators
from ChatApp.Authentication.LogIn.login_bp import LogInForm
from flask import render_template, Blueprint, url_for, request, flash, redirect

signup_bp = Blueprint('signup_bp', __name__, static_folder='static', template_folder='templates')


# registration form
class RegistrationForm(LogInForm):
    username = StringField("Enter Username", [validators.Length(min=4, max=20)])
    password = PasswordField("Password", [validators.InputRequired(),
                                          validators.EqualTo('confirm_password', message="Passwords Must Match")])
    confirm_password = PasswordField("Repeat Password")


@signup_bp.route('/signup', methods=['POST', 'GET'])
def signup():
    form = RegistrationForm(request.form)
    page_title = "Sign Up"

    if request.method == 'POST' and form.validate():
        from ChatApp import app
        app.logger.info("Validation Complete, now posting to db")
        kwargs = {
            'email': request.form['email'],
            'username': request.form['username'],
            'password': request.form['password'],
            'secret_key': request.form['secret_key']
        }
        from ChatApp import mysql
        connection = mysql.connect()
        cursor = connection.cursor()
        check_user_exists = cursor.execute('SELECT user_email FROM users WHERE user_email = (%s)',
                                           request.form['email'])
        app.logger.info("There exists " + str(check_user_exists) + " users with this email:" + request.form['email'])

        if check_user_exists > 0:
            flash('Sorry user already exists! Try a different email, or try to ')
            return render_template('signup.html', form=form, page_title=page_title)
        else:
            cursor.execute('INSERT INTO users (user_email, user_name, user_password) VALUES (%s,%s,%s)',
                           (request.form['email'], request.form['username'], request.form['password']))
            connection.commit()
            cursor.close()
            connection.close()
            app.logger.info("db connection closed")
            return redirect(url_for('chatter_bp.show_posts'))
    return render_template('signup.html', form=form, page_title=page_title)


@signup_bp.route('/red_login')
def try_login():
    return redirect(url_for("signup_bp.signup"))
