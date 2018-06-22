from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from wtforms import Form, StringField, validators

book_club_bp = Blueprint('book_club_bp', __name__, static_folder='static', template_folder='templates',
                         url_prefix='/bookclub')


class BookClubRegistration(Form):
    book_club_name = StringField("Enter Book Club Name", [validators.Length(min=5, max=255)])
    book_name = StringField("Enter The Current book", [validators.Length(min=5, max=255)])
    book_author = StringField("Enter Book Author", [validators.Length(min=4, max=50)])
    book_isbn = StringField("Enter Book ISBN", [validators.Length(min=10, max=25)])
    book_category = StringField("Give Book Category", [validators.Length(min=5, max=55)])
    book_review = StringField("Give Book Review")


@book_club_bp.route('/create-book-club', methods=['POST', 'GET'])
def create_book_club():
    page_title = 'Create Book Club'
    form = BookClubRegistration(request.form)

    if 'user' in session:

        if request.method == 'POST' and form.validate():

            from ChatApp import app
            from ChatApp import mysql
            app.logger.info("Validation complete, now posting to db")

            connection = mysql.connect()
            cursor = connection.cursor()
            app.logger.info("db connection established!")

            cursor.execute('SELECT name FROM book_club WHERE name = (%s)', request.form['book_club_name'])
            name = str(cursor.fetchone())
            formatted_book_club_name = format_db_string(name)
            app.logger.info("name fetched from db is " + str(formatted_book_club_name) + " and user input is "
                            + str(request.form['book_club_name']))

            if formatted_book_club_name == request.form['book_club_name']:
                form.book_club_name.errors = ['Sorry Book Club already exists, try a different name']
                return render_template('base_book_club_register.html', form=form, page_title=page_title)

            else:
                cursor.execute('INSERT INTO book_club (name) VALUES (%s)', request.form['book_club_name'])
                last_book_club_inserted = cursor.lastrowid
                cursor.execute('INSERT INTO book (title, author, isbn, review, category) VALUES (%s,%s,%s,%s,%s)',
                               (request.form['book_name'], request.form['book_author'], request.form['book_isbn'],
                                request.form['book_review'], request.form['book_category']))
                last_book_inserted = cursor.lastrowid
                connection.commit()

                # populate the link tables
                #  get user in session
                session['user'] = session.get('user')
                cursor.execute('SELECT (email) From user WHERE username = (%s)', session['user'])
                user_id = str(cursor.fetchone())

                app.logger.info(
                    'The user in session is : ' + str(session['user']) + " and has user id of " + str(user_id) +
                    '\nThe id of last book club created is: ' + str(last_book_club_inserted) +
                    '\nThe id of the last book created is: ' + str(last_book_inserted))

                # update book_club_book information
                cursor.execute('INSERT INTO book_club_book (book_club_id, book_id) VALUES (%s,%s)',
                               (last_book_club_inserted, last_book_inserted))
                connection.commit()

                # update book_club_users information by adding the book_club_id
                formatted_user_email = format_db_string(user_id)

                cursor.execute('INSERT INTO book_club_user (email, book_club_id) VALUES (%s,%s)',
                               (formatted_user_email, last_book_club_inserted))
                connection.commit()

                session['admin'] = formatted_user_email
                print(session['admin'])

                cursor.execute('INSERT INTO  admin (email, book_club_id) VALUES (%s,%s)',
                               (formatted_user_email, last_book_club_inserted))
                connection.commit()
                cursor.close()

                connection.close()
                app.logger.info("db connection closed")

                flash('Book Club added...')
                return redirect(url_for('dashboard_bp.dashboard'))

        return render_template('base_book_club_register.html', form=form, page_title=page_title)
    else:
        flash('Sorry, your session expired. Log in again')
        return render_template('base_book_club_register.html', form=form, page_title=page_title)


@book_club_bp.route('/join-book-club/', methods=['POST', 'GET'])
def join_book_club():
    session['user'] = session.get('user')
    session['user_id'] = session.get('user_id')
    from ChatApp import app, mysql
    connection = mysql.connect()
    cursor = connection.cursor()

    if session['user']:
        if request.method == 'POST':
            print(request.form.getlist('book_clubs'))

            # check in the admin table for the admins of selected book clubs
            for book_club_id in request.form.getlist('book_clubs'):
                cursor.execute('SELECT admin_id FROM admin WHERE book_club_id = (%s)', book_club_id)
                admin_list = [dict(id=row[0]) for row in cursor.fetchall()]
                app.logger.info('THIS IS THE ADMIN LIST FOR THE BOOK CLUBS USER REQUESTED TO JOIN ' + str(admin_list))

                # get name of the book club user requested to join
                cursor.execute('SELECT name FROM book_club WHERE book_club_id = (%s)', book_club_id)
                book_club_name = [dict(name=row[0]) for row in cursor.fetchall()]
                app.logger.info('HERE ARE THE NAMES OF THE BOOK CLUBS USER REQUESTED TO JOIN ' + str(book_club_name))

                #     send messages to all the admins mentioned.
                #     create a table to store the message and the admin can fetch them later
                join_request = "Hello there! i am " + str(session['user']) + \
                               " and would love to join your book club," + str(book_club_name) \
                               + "kindly accept my request. Thank you in advance."

                for admin in admin_list:
                    a = admin.get('id')
                    print(admin)
                    cursor.execute('INSERT INTO book_club_join_request (book_club_id, admin_id, email, request_msg) '
                                   'VALUES (%s, %s, %s, %s)', (book_club_id, a, session['user_id'], join_request))
            connection.commit()

            flash('Your requests have been sent to the relevant book club admins')
            return redirect(url_for('dashboard_bp.dashboard'))

            # return 'PROCESSING REQUEST'
        else:
            page_title = 'Join A Book Club'
            # display the available book clubs for the user
            cursor.execute('SELECT name, book_club_id FROM book_club')
            book_club = [dict(name=row[0], id=row[1]) for row in cursor.fetchall()]

            app.logger.info('the following book clubs were fetched: ' + str(book_club))

            return render_template('join_book_club.html', page_title=page_title, book_club_list=book_club)
    return redirect(url_for('login_bp.login'))


@book_club_bp.route('/approve-join-request', methods=['GET', 'POST'])
def approve_join_request():
    page_title = 'Approve Join Request'
    from ChatApp import app, mysql
    connection = mysql.connect()
    cursor = connection.cursor()

    session['admin'] = session.get('admin')

    if session['admin']:
        if request.method == 'POST':
            app.logger.info('THE ADMIN IN SESSION IS: ' + str(session['admin']))
            # we need to check those accepted and add them to the book club

            for request_message in request.form.getlist('request_message'):
                print(request_message)

                if request.form.getlist('submit'):
                    # insert into book_club_user the approved users
                    for request_approved in request.form.getlist('request_message'):
                        cursor.execute('SELECT email FROM book_club_join_request WHERE book_club_id = (%s)',
                                       request_approved)
                        user_email = [dict(email=row[0]) for row in cursor.fetchall()]
                        app.logger.info('EMAILS OF USERS WISHING TO JOIN ARE ' + str(user_email))

                        for user in user_email:
                            cursor.execute('INSERT INTO book_club_user (book_club_id, email) VALUES (%s,%s)',
                                           (request_approved, user.get('email')))

                            app.logger.info('*** THE USER APPROVED IS : ' + str(user) +
                                            "TO JOIN BOOK CLUB OF ID  : " + str(request_approved))
                        connection.commit()
                    app.logger.info(
                            'THIS WERE THE ACCEPTED REQUESTS ' + str(request.form.getlist('request_message')))
                    flash('The Requests were successfully granted....')
                    return redirect(url_for('book_club_bp.approve_join_request'))

                elif request.form.getlist('reset'):
                    # send message to the relevant parties
                    for request_denied in request.form.getlist('request_message'):
                        app.logger.info('THESE REQUESTS WERE DECLINED ' + str(request_denied))
                    app.logger.info('THIS REQUEST WAS DENIED ' + str(request.form.getlist('request_message')))
                    flash('The Requests were successfully declined....')
                    return redirect(url_for('book_club_bp.approve_join_request'))

            return redirect(url_for('book_club_bp.approve_join_request'))

        else:
                app.logger.info('THE ADMIN IN SESSION IS: ' + str(session['admin']))
                # send request to the admins
                cursor.execute('SELECT a.name from book_club a JOIN book_club_join_request b USING (book_club_id)')
                book_club = cursor.fetchall()
                print(book_club)

                cursor.execute('SELECT admin_id FROM admin WHERE email = (%s)', session['admin'])
                admins = cursor.fetchall()
                app.logger.info('HERE IS THE ID OF THE CURRENT ADMIN ' + str(admins))

                for admin in admins:
                    cursor.execute('SELECT request_msg, book_club_id FROM book_club_join_request WHERE admin_id = (%s)',
                                   admin)
                    request_messages = [dict(request=row[0], id=row[1]) for row in cursor.fetchall()]

                    return render_template('admin_dashboard.html', page_title=page_title,
                                           request_messages=request_messages)
    flash('You are not logged in or ')
    return redirect(url_for('login_bp.login'))


# UDFs
def format_db_string(db_string):
    unwanted_char = ["'", "(", ")", ","]
    for i in range(len(unwanted_char)):
        db_string = db_string.replace(unwanted_char[i], "")
    return db_string
