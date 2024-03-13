from flask import Flask, abort, render_template, redirect, request, session, url_for
from hw03.models import db, User
from markupsafe import escape
from validate_email import validate_email
import sqlalchemy


app = Flask(__name__)
app.secret_key = '1f9ae2a24f5b43b3b8f71fc096b8aee7ea676d3a18e54c30898d9e19996fd69a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///geekbrains.db'
db.init_app(app)


@app.route('/')
def index():
    context = {
        'title': 'The Brand of luxurious fashion',
        'promo_image': 'promo',
        'promo_title': 'The Brand'
    }
    return render_template('index.html', **context)


@app.cli.command("init-db")
def init_db():
    db.drop_all()
    db.create_all()
    print('DB initialized')


@app.route('/women/')
def women():
    context = {
        'title': 'Women | The Brand of luxurious fashion',
        'promo_image': 'promo_women_main',
        'promo_title': 'Women'
    }
    return render_template('women.html', **context)


@app.route('/women/jackets/')
def women_jackets():
    context = {
        'title': 'Women Jackets | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/women/polos/')
def women_polos():
    context = {
        'title': 'Women Polos | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/women/t-shirts/')
def women_tshirts():
    context = {
        'title': 'Women T-Shirts | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/women/shirts/')
def women_shirts():
    context = {
        'title': 'Women Shirts | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/men/')
def men():
    context = {
        'title': 'Men | The Brand of luxurious fashion',
        'promo_image': 'promo_men_main',
        'promo_title': 'Men'
    }
    return render_template('men.html', **context)


@app.route('/men/bags/')
def men_bags():
    context = {
        'title': 'Men Bags | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/men/denim/')
def men_denim():
    context = {
        'title': 'Men Denim | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/men/t-shirts/')
def men_tshirts():
    context = {
        'title': 'Men T-Shirts| The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/kids/')
def kids():
    context = {
        'title': 'Kids | The Brand of luxurious fashion',
        'promo_image': 'promo_kids_main',
        'promo_title': 'Kids'
    }
    return render_template('kids.html', **context)


@app.route('/kids/jackets/')
def kids_jackets():
    context = {
        'title': 'Kids Jackets | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/kids/polos/')
def kids_polos():
    context = {
        'title': 'Kids Polos | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/kids/t-shirts/')
def kids_tshirts():
    context = {
        'title': 'Kids T-Shirts | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/kids/shirts/')
def kids_shirts():
    context = {
        'title': 'Kids Shirts | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/kids/bags/')
def kids_bags():
    context = {
        'title': 'Kids bags | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/accessories/')
def accessories():
    context = {
        'title': 'Accessories | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)


@app.route('/user/', methods=['GET', 'POST'])
def user():
    context = {
        'title': 'User login | The Brand of luxurious fashion',
        'promo_image': 'promo_user_main',
        'promo_title': 'User login',
        'no_title_text': True,
        'no_info_bar': True
    }
    if request.method == 'POST':
        user_email = escape(request.form.get('user_email'))
        user_password = escape(request.form.get('user_password'))
        marketplace_user = User.query.filter_by(user_email=user_email).first()
        if not marketplace_user:
            context['error_message'] = ['No such user']
            return render_template('user_login.html', **context)
        if not marketplace_user.password_is_valid(user_password):
            context['error_message'] = ['Password is invalid']
            return render_template('user_login.html', **context)
        session['user_id'] = marketplace_user.get_user_id()
        session['user_firstname'] = marketplace_user.get_user_firstname()
        session['user_lastname'] = marketplace_user.get_user_lastname()
        session['user_email'] = marketplace_user.get_user_email()
        session['user_status'] = 'registered'
    elif 'user_id' not in session:
        return render_template('user_login.html', **context)
    return redirect(f'/user/{session["user_id"]}/')


def invalid_user_input(context, user_firstname, user_lastname, user_email, user_password1, user_password2,
                       check_user_email=True):
    """
    Checks user profile input and edit context if errors detected
    :param context: Context parameters
    :param user_firstname: User firstname
    :param user_lastname: User lastname
    :param user_email: User e-mail
    :param user_password1: User password 1
    :param user_password2: User password 2
    :param check_user_email: Check e-mail validation
    :return: True if errors was detected otherwise returns False
    """
    context['error_message'] = []
    if check_user_email and not check_email(user_email):
        context['error_message'].append('Your e-mail is invalid.')
        del context['user_email']
    if check_user_email and User.query.filter_by(user_email=request.form.get('user_email')).first():
        context['error_message'].append('This e-mail is unavailable.')
        del context['user_email']
    if not check_name(user_firstname):
        context['error_message'].append('Your firstname is too long.')
        del context['user_firstname']
    if not check_name(user_lastname):
        context['error_message'].append('Your lastname is too long.')
        del context['user_lastname']
    if user_password1 != user_password2:
        context['error_message'].append('Passwords do not match.')
    if len(context['error_message']) == 0:
        del context['error_message']
        return False
    return True


@app.route('/user/register/', methods=['GET', 'POST'])
def user_register():
    if 'user_id' in session:
        return redirect(f'/user/{session["user_id"]}/')

    context = {
        'title': 'Register user | The Brand of luxurious fashion',
        'promo_image': 'promo_user_main',
        'promo_title': 'Register new User',
        'no_title_text': True,
        'no_info_bar': True
    }

    if request.method == 'POST':
        context['user_firstname'] = request.form.get('user_firstname')
        context['user_lastname'] = request.form.get('user_lastname')
        context['user_email'] = request.form.get('user_email')

        if invalid_user_input(
            context,
            request.form.get('user_firstname'),
            request.form.get('user_lastname'),
            request.form.get('user_email'),
            request.form.get('user_password1'),
            request.form.get('user_password2')
        ):
            return render_template('user_register.html', **context)

        user_id = add_user(
            request.form.get('user_firstname'),
            request.form.get('user_lastname'),
            context['user_email'],
            request.form.get('user_password1')
        )

        if user_id == -1:
            context['error_message'] = ['Database error. Can not register user. Try to register later']
            return render_template('user_register.html', **context)

        session['user_id'] = user_id
        session['user_firstname'] = context['user_firstname']
        session['user_lastname'] = context['user_lastname']
        session['user_email'] = context['user_email']
        session['user_status'] = 'newbie'

        return redirect(f'/user/{session["user_id"]}/')

    return render_template('user_register.html', **context)


@app.route('/user/logout/')
def user_logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/user/<int:user_id>/', methods=['GET', 'POST'])
def user_profile(user_id: int):
    try:
        if user_id != session['user_id']:
            abort(404)
    except KeyError:
        abort(404)

    context = {
        'title': f'{session["user_firstname"]} profile | The Brand of luxurious fashion',
        'promo_image': 'promo_user_main',
        'promo_title': f'Welcome {session["user_firstname"]}',
        'no_title_text': True,
        'no_info_bar': True,
        'user_id': session['user_id'],
        'user_firstname': session['user_firstname'],
        'user_lastname': session['user_lastname'],
        'user_email': session['user_email']
    }

    if request.method == 'GET':
        if session['user_status'] == 'newbie':
            context['success_message'] = 'Registration completed.'
        session['user_status'] = 'registered'
        return render_template('user_profile.html', **context)

    if request.form.get('action') and request.form.get('action') == 'logout':
        return redirect(url_for('user_logout'))

    if invalid_user_input(
        context,
        request.form.get('user_firstname'),
        request.form.get('user_lastname'),
        request.form.get('user_email'),
        request.form.get('user_password1'),
        request.form.get('user_password2'),
        session['user_email'] != request.form.get('user_email')
    ):
        return render_template('user_profile.html', **context)

    marketplace_user = User.query.filter_by(user_id=int(session['user_id'])).first()
    if not marketplace_user.password_is_valid(request.form.get('user_password')):
        context['error_message'] = ['Password is invalid']
        return render_template('user_profile.html', **context)

    marketplace_user.set_user_firstname(request.form.get('user_firstname'))
    marketplace_user.set_user_lastname(request.form.get('user_lastname'))
    marketplace_user.set_user_email(request.form.get('user_email'))
    if request.form.get('user_password1') != '':
        marketplace_user.set_user_password(request.form.get('user_password1'))
    db.session.commit()

    session['user_firstname'] = marketplace_user.get_user_firstname()
    session['user_lastname'] = marketplace_user.get_user_lastname()
    session['user_email'] = marketplace_user.get_user_email()
    session['user_status'] = 'updated'
    context['user_firstname'] = session['user_firstname']
    context['user_lastname'] = session['user_lastname']
    context['user_email'] = session['user_email']
    context['success_message'] = 'User information updated.'

    return render_template('user_profile.html', **context)


def check_email(email: str) -> bool:
    """
    :param email: e-mail string for validation
    :return: True if e-mail is valid or False if it invalid
    """
    return (validate_email(email) or False) and len(email) < 128


def check_name(name: str) -> bool:
    """
    :param name: username for validation
    :return: True if username is valid or False if it invalid
    """
    return isinstance(name, str) and len(name) <= 128


def add_user(user_firstname: str, user_lastname: str, user_email: str, user_password: str) -> int:
    """
    Adds user to Database.
    :param user_firstname: User firstname
    :param user_lastname: User lastname
    :param user_email: User e-mail
    :param user_password: User password
    :return: user id or error code
    """
    marketplace_user = User(user_firstname, user_lastname, user_email, user_password)
    try:
        db.session.add(marketplace_user)
        db.session.commit()
        return marketplace_user.get_user_id()
    except sqlalchemy.exc.InterfaceError:
        return -1


@app.errorhandler(404)
def page_not_found(e):
    context = {
        'title': 'Page not found | The Brand of luxurious fashion',
        'promo_image': '404',
        'promo_title': 'Page not found',
        'no_title_text': True,
        'no_info_bar': True,
        'error_message': e
    }
    app.logger.warning(e)
    return render_template('404.html', **context), 404


@app.errorhandler(500)
def server_error(e):
    context = {
        'title': 'Server error | The Brand of luxurious fashion',
        'promo_image': '404',
        'promo_title': 'Server error',
        'no_title_text': True,
        'no_info_bar': True,
        'error_message': e
    }
    app.logger.warning(e)
    return render_template('500.html', **context), 500
