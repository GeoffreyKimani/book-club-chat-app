from flask import Flask
from flaskext.mysql import MySQL
from flask_wtf.csrf import CSRFProtect
from .Welcome.index_bp import home_bp
from .Authentication.SignUp.signup_bp import signup_bp
from .Authentication.LogIn.login_bp import login_bp
from .ChatArea.chatter_bp import chatter_bp

app = Flask(__name__)

# configure the app
mysql = MySQL()
app.secret_key = 'secrets&lies'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jeffkim'
app.config['MYSQL_DATABASE_DB'] = 'BookClubDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
csrf = CSRFProtect(app)
csrf.init_app(app)

# register app blueprints
app.register_blueprint(home_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(chatter_bp)
