from flask import Flask
import os
from flaskext.mysql import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from .Welcome.index_bp import home_bp
from .Authentication.SignUp.signup_bp import signup_bp
from .Authentication.LogIn.login_bp import login_bp
from .ChatArea.chatter_bp import chatter_bp
from .Dashboard.dashboard_bp import dashboard_bp
from .BookClubs.book_club_bp import book_club_bp
from .BookClubBooks.book_club_book import book_club_book_bp

app = Flask(__name__)

# configure the app
mysql = MySQL()
app.secret_key = os.urandom(24)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jeffkim'
app.config['MYSQL_DATABASE_DB'] = 'book_club'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
csrf = CSRFProtect(app)
csrf.init_app(app)
bcrypt = Bcrypt(app)

# register app blueprints
app.register_blueprint(home_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(chatter_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(book_club_bp)
app.register_blueprint(book_club_book_bp)
