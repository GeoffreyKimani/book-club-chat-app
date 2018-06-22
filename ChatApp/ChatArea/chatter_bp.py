from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from wtforms import Form, StringField, validators
from ChatApp.Authentication.LogIn.login_bp import format_db_string
from collections import defaultdict

chatter_bp = Blueprint('chatter_bp', __name__, static_folder='static', template_folder='templates')


class PostForm(Form):
    title = StringField("Post Title ", [validators.InputRequired()])
    text = StringField("Post Body", [validators.InputRequired()])


@chatter_bp.route('/index', methods=['POST', 'GET'])
def show_posts():
    # first check if user is in session
    session['user'] = session.get('user')
    session['active_id'] = session.get('active_id')

    if session['user']:
        print(session['active_id'])
        page_title = "Home"

        from ChatApp import app
        app.logger.info('Posts fetched for user ' + str(session['user']))

        # fetch data from the database to display
        from ChatApp import mysql
        connection = mysql.connect()
        cursor = connection.cursor()
        app.logger.info('Checking db to fetch some posts ')

        # first direct the user to a default page since no book club has been selected

        # select_book_club = flash('Please go to dashboard and select a book club to view posts')
        if session.get('active_id'):
            if not session['active_id']:
                return render_template('post_area.html', page_title=page_title)

            else:
                cursor.execute('SELECT post_id, title, text,email FROM post WHERE book_club_id=(%s)',
                               (session['active_id']))

                posts = [dict(post_id=row[0], title=row[1], text=row[2], email=row[3]) for row in cursor.fetchall()]
                print(posts)

                user_post_list = []
                for post_by_user in posts:
                    print(post_by_user['post_id'])
                    cursor.execute('SELECT email FROM post WHERE post_id = (%s)', post_by_user['post_id'])

                    user_post = [dict(username=row[0]) for row in cursor.fetchall()]
                    print(user_post)

                    # return render_template('post_area.html', page_title=page_title, posts=posts,
                    #                        username=user_post)

                    # create a list to get all the list of dict
                    user_post_list.append(user_post)
                print(user_post_list)

                for name in user_post_list:
                    print(name)

                    return render_template('post_area.html', page_title=page_title, posts=posts, username=name)
        return render_template('post_area.html', page_title=page_title)

    else:
        flash('To continue, please Log In first or ')
        return redirect(url_for('login_bp.login'))


@chatter_bp.route('/add_post', methods=['POST', 'GET'])
def add_post():
    # first check if users are logged in / in session.

    if 'user' in session:
        session['user'] = session.get('user')
        session['active'] = session.get('active')
        session['active_id'] = session.get('active_id')
        print(session['active_id'])
        print(session['active'])

        from ChatApp import app
        app.logger.info('User  ' + str(session['user']) + ' making a post comment.')

        # commit posts to the database
        form = PostForm(request.form)
        if request.method == 'POST' and form.validate():
            from ChatApp import mysql
            connection = mysql.connect()
            cursor = connection.cursor()

            # commit changes to the post
            # take the id of the user in session, take the id of the book_club
            #  capture the user making the post
            cursor.execute('SELECT email FROM user WHERE username=(%s)', session['user'])
            user_email = format_db_string(str(cursor.fetchone()))
            print(user_email)

            if session.get('active_id'):
                if session['active_id']:

                    if cursor.execute('INSERT INTO post (title, text, email, book_club_id ) VALUES (%s,%s,%s,%s)',
                                      (request.form['title'], request.form['text'], user_email, session['active_id'])):
                        connection.commit()
                        from ChatApp import app
                        app.logger.info('Post created by user ' + str(session['user']) + " to book club "
                                        + str(session['active']))

            else:
                return redirect(url_for('chatter_bp.show_posts'))

            flash("Message was successfully posted")
            cursor.close()
            connection.close()

        return redirect(url_for('chatter_bp.show_posts'))
    else:
        flash('To continue, please Log In first or ')
        return redirect(url_for('login_bp.login'))
