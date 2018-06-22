from flask import render_template, request, session, flash, Blueprint, redirect, url_for
from wtforms import Form, validators, StringField
from ChatApp.Authentication.LogIn.login_bp import format_db_string

book_club_book_bp = Blueprint('book_club_book_bp', __name__, static_folder='static', template_folder='templates',
                              url_prefix='/book-club-book')


class BookClubBookRegistration(Form):
    book_name = StringField("Enter The Current book", [validators.Length(min=5, max=255)])
    book_author = StringField("Enter Book Author", [validators.Length(min=4, max=50)])
    book_isbn = StringField("Enter Book ISBN", [validators.Length(min=10, max=25)])
    book_category = StringField("Give Book Category", [validators.Length(min=5, max=55)])
    book_review = StringField("Give Book Review")


@book_club_book_bp.route('/add-book', methods=['GET', 'POST'])
def add_book():
    page_title = 'Add Book'
    form = BookClubBookRegistration(request.form)

    # check if user is in session
    if 'user' in session:

        if request.method == 'POST' and form.validate():
            from ChatApp import app
            app.logger.info('validation complete, now posting to db')
            #    get the user in session
            from ChatApp import mysql
            connection = mysql.connect()
            cursor = connection.cursor()

            session['user'] = session.get('user')
            session['active'] = session.get('active')
            session['active_id'] = session.get('active_id')

            # check the book clubs the user is in and allow them to pick where to add the book

            # we also need to insert into the book table.
            cursor.execute('INSERT INTO book (title, author, isbn, review, category) VALUES (%s,%s,%s,%s,%s)',
                           (request.form['book_name'], request.form['book_author'], request.form['book_isbn'],
                            request.form['book_review'], request.form['book_category']))
            last_book_inserted = cursor.lastrowid
            print(last_book_inserted)
            connection.commit()

            cursor.execute('INSERT INTO book_club_book (book_club_id, book_id) VALUES (%s,%s)',
                           (session['active_id'], last_book_inserted))
            connection.commit()

            app.logger.info('User ' + str(session['user']) + ' added book ' + str(last_book_inserted)
                            + ' to book club ' + str(session['active']))

            flash('Book Added!')
            return redirect(url_for('dashboard_bp.dashboard'))

        return render_template('book_book_club_register.html', form=form, page_title=page_title)

    else:
        flash('Sorry, your session expired. Log in again')
        return render_template('book_book_club_register.html', form=form, page_title=page_title)

