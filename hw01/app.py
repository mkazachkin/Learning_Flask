from flask import Flask,  render_template

app = Flask(__name__)

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
def kids_denim():
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
def kids_accessories():
    context = {
        'title': 'Accessories | The Brand of luxurious fashion'
    }
    return render_template('sales.html', **context)

if __name__ == '__main__':
    app.run(debug=True)