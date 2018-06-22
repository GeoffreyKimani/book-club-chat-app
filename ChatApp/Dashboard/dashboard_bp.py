from flask import Blueprint, render_template, session, url_for, redirect, flash
from ChatApp.Authentication.LogIn.login_bp import format_db_string

dashboard_bp = Blueprint('dashboard_bp', __name__, static_folder='static', template_folder='templates')


@dashboard_bp.route('/dashboard')
# class Dashboard:
def dashboard():
    # global book_club_list
    page_title = "Dashboard"

    session['user'] = session.get('user')
    session['user_id'] = session.get('user_id')

    if session['user']:

        from ChatApp import app
        app.logger.info('User  ' + str(session['user']) + ' accessing dashboard.')

        from ChatApp import mysql
        connection = mysql.connect()
        cursor = connection.cursor()

        # check the book clubs the user is in
        cursor.execute('SELECT b.name, book_club_id FROM book_club b JOIN book_club_user s USING (book_club_id) '
                       'WHERE email = (%s)', session['user_id'])
        book_club_list = [dict(name=row[0], id=row[1]) for row in cursor.fetchall()]
        print(book_club_list)

        book_book_club = []
        for item in book_club_list:
            print(item['id'])

            # check the books available for each of the book_clubs
            # first we will need to get a list of all the book clubs a user is in
            cursor.execute('SELECT b.title FROM book b JOIN book_club_book s USING (book_id)'
                           'WHERE book_club_id = (%s)', item['id'])
            book_book_club = [dict(title=row[0]) for row in cursor.fetchall()]
            print(book_book_club)
        print(book_book_club)
        return render_template('dashboard.html', page_title=page_title,
                               book_club_list=book_club_list, book_book_club=book_book_club)
    else:
        flash('To continue, please Log In first or ')
        return redirect(url_for('login_bp.login'))


@dashboard_bp.route('/book-club-selection/<id>')
def book_club_selection(id):
    """to fetch user specific posts, we need to decouple the book clubs and get the active book club a user is in
    at the moment """

    # create a session dictionary storing a key value pair of the book_club_id and book_id.
    #  this will help fetch posts from specified books and clubs

    session.pop('active', None)

    # perform a query to retrieve book_club name with the given id

    from ChatApp import mysql, app
    connection = mysql.connect()
    cursor = connection.cursor()

    cursor.execute('SELECT name FROM book_club WHERE book_club_id = (%s)', id)
    book_club_name = format_db_string(str(cursor.fetchone()))
    app.logger.info('The book club selected is ' + str(book_club_name))

    session['active'] = book_club_name
    session['active_id'] = id
    session['admin'] = session.get('admin')
    print(session['admin'])
    if session['active']:
        print(session['active_id'])
        return redirect(url_for('chatter_bp.show_posts'))


@dashboard_bp.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('active', None)
    session.pop('active_id', None)
    session.pop('admin', None)
    flash('You are now logged out!')
    return redirect(url_for('home_bp.index'))


@dashboard_bp.route('/addbook')
def red_add_book():
    return redirect(url_for('book_club_book_bp.add_book'))
