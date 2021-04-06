#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 16:09:50 2021

@author: Petec0x0
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError
from market.model import User

class RegisterForm(FlaskForm):
        username = StringField(label='Username', validators=[DataRequired(), Length(min=2, max=20)])
        email = StringField(label='Email Address', validators=[Email(), DataRequired()])
        password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
        password_confirm = PasswordField(label='Confirm Password', validators=[EqualTo('password')])
        submit = SubmitField(label='Create Account')
        
        # custom validation to check if username already exist
        def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exist.')
                
        # custom validation to check if email address already exist
        def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email Address already exist.')
                
class LoginForm(FlaskForm):
        username = StringField(label='Username', validators=[DataRequired(), Length(min=2, max=20)])
        password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
        submit = SubmitField(label='Login')
        
class PurchaseForm(FlaskForm):
        purchase_item = SubmitField(label='Purchase Item')
                
class SellForm(FlaskForm):
        sell_item = SubmitField(label='Sell Item')