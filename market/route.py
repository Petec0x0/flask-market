from flask import render_template, flash, redirect, url_for
from market import app, db
from market.model import Item, User
from market.forms import RegisterForm

@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/market')
def market():
    # get all Item from the database using the Item model/class
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=('GET', 'POST'))
def register():
    # get the RegisterForm class from form.py
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data)   
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('market'))
        
        
    if form.errors:
        for errors in form.errors.values():
            flash(f'Error : {errors[0]}', category='danger') 
    
    return render_template('register.html', form=form)