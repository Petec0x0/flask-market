#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 21:02:08 2021

@author: petec0x0
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    barcode = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(), unique=True, nullable=False)


@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/market')
def market():
    items = Item.query.all()
    return render_template('market.html', items=items)

