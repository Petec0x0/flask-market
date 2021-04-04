from flask import render_template, flash, redirect, url_for
from market import app, db
from market.model import Item, User
from market.forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

@app.route('/home')
@app.route('/')
def index():
    # render the index.html template
    return render_template('index.html')

@app.route('/market')
@login_required
def market():
    # get all Item from the database using the Item model/class
    items = Item.query.all()
    # render the market.html template
    return render_template('market.html', items=items)

@app.route('/register', methods=('GET', 'POST'))
def register():
    # get the RegisterForm class from form.py
    form = RegisterForm()
    """
        validate the form using all the written validations from the 
        RegisterForm class
    """
    if form.validate_on_submit():
        # create a user object from the User class/model
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data))   
        
        # add and commit changes to the database
        db.session.add(user)
        db.session.commit()
        
        flash("User created successfully! login to continue", category='success')
        return redirect(url_for('market'))
        
    # check for error messages     
    if form.errors:
        # ilterate and flash error messages if it exist
        for errors in form.errors.values():
            flash(f'Error : {errors[0]}', category='danger') 

    # render the register.html template along with the form instance
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    # get the LoginForm class from form.py
    form = LoginForm()
    """
        validate the form using all the written validations from the 
        LoginForm class
    """
    if form.validate_on_submit():
        # authenticate user if correct credentials is entered
        user = User.query.filter_by(username=form.username.data).first()
        
        # check if user exist and if password is correct
        if user and check_password_hash(user.password, form.password.data):
            # login the user
            login_user(user) 
            # flash success message for the user
            flash("User logged in successfully", category='success')
            # redirect user to market page
            return redirect(url_for('market'))
        else:
            # flash error message is authentication fails
            flash("Username or Password Incorrect", category='danger')
            
    
    # check for error messages     
    if form.errors:
        # ilterate and flash error messages if it exist
        for errors in form.errors.values():
            flash(f'Error : {errors[0]}', category='danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    # render the market.html template
    logout_user()
    # flash info message about the logout
    flash('Signed out successfully!', category='info')
    # redirect to home page after logout
    return redirect(url_for('index'))
    