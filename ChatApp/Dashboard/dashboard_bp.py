from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard_bp', __name__, static_folder='static', template_folder='templates')


@dashboard_bp.route('/dashboard')
def dashboard():
    page_title = "Dashboard"
    return render_template('dashboard.html', page_title=page_title)
