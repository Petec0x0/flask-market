from flask import render_template
from market import app
from market.model import Item

@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/market')
def market():
    items = Item.query.all()
    return render_template('market.html', items=items)
