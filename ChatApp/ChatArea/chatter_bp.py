from flask import render_template, request, redirect, url_for, flash, Blueprint
from wtforms import Form, StringField, validators

chatter_bp = Blueprint('chatter_bp', __name__, static_folder='static', template_folder='templates')


class PostForm(Form):
    title = StringField("Post Title ", [validators.InputRequired()])
    text = StringField("Post Body", [validators.InputRequired()])


@chatter_bp.route('/index', methods=['POST', 'GET'])
def show_posts():
    # fetch data from the database to display
    page_title = "Home"
    from ChatApp import mysql
    connection = mysql.connect()
    cursor = connection.cursor()
    print("checking database")
    if cursor.execute('select title, text from posts order by id'):
        print("fetched some data")
    # cursor.execute('SELECT user_name FROM users WHERE ')
    posts = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
    print(posts)

    return render_template('post_area.html', page_title=page_title, posts=posts)


@chatter_bp.route('/add_post', methods=['POST', 'GET'])
def add_post():
    # commit posts to the database
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        from ChatApp import mysql
        connection = mysql.connect()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO posts (title, text) VALUES (%s,%s)',
                       (request.form['title'], request.form['text']))
        connection.commit()
        # flash("Message was successfully posted")
        cursor.close()
        connection.close()
    return redirect(url_for('chatter_bp.show_posts'))

# def home():
#     kwargs = {
#         'title': request.form['title'],
#         'text': request.form['text']
#     }
#     show_posts()
#     # add_post(form)
