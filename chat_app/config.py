from flask import Flask
from flaskext.mysql import MySQL


# secret_key = 'Password'

MYSQL_DATABASE_USER = 'jeffkim'
MYSQL_DATABASE_PASSWORD = 'jeffkim'
MYSQL_DATABASE_DB = 'BookClubDB'
MYSQL_DATABASE_HOST = 'localhost'


app = Flask(__name__)
mysql = MySQL()
app.secret_key = 'secrets&lies'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jeffkim'
app.config['MYSQL_DATABASE_DB'] = 'BookClubDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


