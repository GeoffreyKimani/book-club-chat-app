from flask import render_template, Blueprint, url_for, request, flash, redirect
from flask_login import current_user, login_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from ChatApp.Models.database import BaseModel

signup_bp = Blueprint('signup_bp', __name__, static_folder='static', template_folder='templates')


# registration form
class RegistrationForm(FlaskForm):
    first_name = StringField("Enter First name", [Length(min=3, max=15)])
    last_name = StringField("Enter Surname", [Length(min=4, max=15)])
    username = StringField("Enter Username", [Length(min=4, max=20)])
    email = StringField('email', [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired(),
                                          EqualTo('confirm_password', message="Passwords Must Match")])
    confirm_password = PasswordField("Repeat Password")

    # from ChatApp.Models.user import User
    def validate_username(self, username):
        from ChatApp.Models.user import User
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValueError('Please use a different username.')

    def validate_email(self, email):
        from ChatApp.Models.user import User
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValueError('Please use a different email.')


@signup_bp.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('signup_bp.signup'))

    form = RegistrationForm(request.form)
    page_title = "Sign Up"

    if form.validate_on_submit():
        from ChatApp.Models.user import User
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
        )
        user.hash_password(form.password.data)
        BaseModel.db.session.add(user)
        BaseModel.db.session.commit()
        login_user(user, remember=False)
        flash("Congratulations, you are now registered!")
        return redirect(url_for('chatter_bp.show_posts'))
    return render_template('signup.html', form=form, page_title=page_title)
