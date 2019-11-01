from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

from ChatApp.Models.user import User

login_bp = Blueprint('login_bp', __name__, static_folder='static', template_folder='templates')


class LogInForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    remember_me = BooleanField('Remember Me')


@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    title = "Log In"
    form = LogInForm(request.form)

    if current_user.is_authenticated:
        return redirect(url_for('chatter_bp.show_posts'))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash("User not registered")
        elif not user.verify_password(form.password.data):
            flash("Wrong password, try again!")
        else:
            login_user(user, remember=form.remember_me.data)
            flash("Welcome {0}, happy to remember me you!".format(form.username.data))
            return redirect(url_for('chatter_bp.show_posts'))
    return render_template('login.html', title=title, form=form)


@login_bp.route('/red_signup')
def try_signup():
    return redirect(url_for("login_bp.login"))

def say():
    return 'k'
