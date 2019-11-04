from flask import render_template, Blueprint, redirect, url_for

home_bp = Blueprint('home_bp', __name__, static_folder='static', template_folder='templates')


@home_bp.route('/')
def index():
    title = 'Welcome'
    return render_template('index.html', title=title, home='current')


# @home_bp.route('/red_login')
# def redirect_login():
#     return redirect(url_for("login_bp.login"))
#
#
# @home_bp.route('/red_signup')
# def redirect_signup():
#     return redirect(url_for("signup_bp.signup"))
#
#
# @home_bp.route('/red_dashboard')
# def to_dashboard():
#     return redirect(url_for("dashboard_bp.dashboard"))
