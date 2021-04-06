from flask import render_template, flash, redirect, url_for, request
from market import app, db
from market.model import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseForm, SellForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

@app.route('/home')
@app.route('/')
def index():
    # render the index.html template
    return render_template('index.html')

@app.route('/market', methods=('GET', 'POST'))
@login_required
def market():
    # purchase form
    purchse_form = PurchaseForm()
    # sell form
    sell_form = SellForm()
    
    
    # check if the sent http request is GET or POST using the flask.request library
    if request.method == 'POST':
        # check which of the forms the request came from
        if request.form.get('purchase_item'):
            # if the request came from Purchase form then ...
            item_to_purchase = Item.query.filter_by(id=request.form.get('item_id')).first()
            # check if user can afford the item using the "can_buy_item" method
            if current_user.can_buy_item(item_to_purchase):
                # buy item or change ownership using the "buy" method
                item_to_purchase.buy(current_user)
                # flash a message if item was purchased successfully
                flash('Well done! Item purchased successfully', category='success')
            else:
                # flash an error message if the user can't afford the item
                flash('Sorry! you cannot afford this item', category='danger')
        elif request.form.get('sell_item'):
            # if request came from Sell form then ...
            item_to_sell = Item.query.filter_by(id=request.form.get('item_id')).first()
            """ check if the current user have ownership to the item using the
                "can_sell_item" method
            """
            if current_user.can_buy_sell(item_to_sell):
                # sell item or change ownership using the "sell" method
                item_to_sell.sell(current_user)
                # flash a message if item was purchased successfully
                flash('Well done! Item sold successfully', category='success')
            else:
                # flash an error message if the user does not own the item
                flash('Sorry! Something went wrong', category='danger')
        
        return redirect(url_for('market'))
    elif request.method == 'GET':
        # get Items not owned by any user from the database using the Item model/class
        items = Item.query.filter_by(owner_id=None)
        # get user owned items
        owned_items = Item.query.filter_by(owner_id=current_user.id)
        # render the market.html template
        return render_template('market.html', items=items, owned_items=owned_items, purchse_form=purchse_form, sell_form=sell_form)

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
    