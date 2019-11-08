from flask import Blueprint, render_template, session, url_for, redirect, flash
from flask_login import login_required, current_user, logout_user

from ChatApp.Models.user import User

# from ChatApp.Authentication.LogIn.login_bp import format_db_string

dashboard_bp = Blueprint('dashboard_bp', __name__, static_folder='static', template_folder='templates')


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    title = "Dashboard"
    user = User.query.filter(User.id == current_user.id).first()

    book_clubs = []
    for book_club in user.book_club:
        book_club_dict = {'name': book_club.name}

        for book in book_club.books:
            book_club_dict['book'] = book.title

        book_clubs.append(book_club_dict)

    return render_template('dashboard.html', title=title, dashboard='current',
                           book_clubs=book_clubs)


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
    logout_user()
    flash('You are now logged out!')
    return redirect(url_for('home_bp.index'))


@dashboard_bp.route('/addbook')
def red_add_book():
    return redirect(url_for('book_club_book_bp.add_book'))
