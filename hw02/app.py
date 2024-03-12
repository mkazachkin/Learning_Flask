from flask import Flask, render_template, redirect, request, session, url_for
from markupsafe import escape
from validate_email import validate_email

app = Flask(__name__)
app.secret_key = '1f9ae2a24f5b43b3b8f71fc096b8aee7ea676d3a18e54c30898d9e19996fd69a'


@app.route('/')
def index():
    context = {
        'title': 'The Brand of luxurious fashion',
        'promo_image': 'promo',
        'promo_title': 'The Brand'
    }
    return render_template('index.html', **context)


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
    if request.method == 'POST':
        if request.form.get('action') == 'logout':
            return user_logout()
        username = escape(request.form.get('username'))
        user_email = escape(request.form.get('user_email'))
        if check_name(username) and check_email(user_email):
            session['username'] = username
            session['user_email'] = user_email
        return redirect(url_for('user'))
    elif 'username' not in session:
        context = {
            'title': 'User login | The Brand of luxurious fashion',
            'promo_image': 'promo_user_main',
            'promo_title': 'User login',
            'no_title_text': True,
            'no_info_bar': True
        }
        return render_template('user_login.html', **context)
    else:
        context = {
            'title': f'{session["username"]} profile | The Brand of luxurious fashion',
            'promo_image': 'promo_user_main',
            'promo_title': f'Welcome {session["username"]}',
            'no_title_text': True,
            'no_info_bar': True,
            'username': session["username"],
            'user_email': session["user_email"]
        }
        return render_template('user_profile.html', **context)


@app.route('/user/logout/')
def user_logout():
    session.pop('username', None)
    session.pop('user_email', None)
    return redirect(url_for('index'))


def check_email(email: str) -> bool:
    """
    :param email: e-mail string for validation
    :return: True if e-mail is valid or False if it invalid
    """
    return validate_email(email) or False


def check_name(name: str) -> bool:
    """
    :param name: username for validation
    :return: True if username is valid or False if it invalid
    """
    return isinstance(name, str) and name != '' and name != 'logout' and len(name) < 128


@app.post('/user/')
def user_post():
    return ''


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


if __name__ == '__main__':
    app.run(debug=True)
