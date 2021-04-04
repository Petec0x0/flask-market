#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 21:02:08 2021

@author: petec0x0
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SECRET_KEY"] = "96tuvh6dhvtxx5dt5e5drwsdredxfe5etdtd5354wr"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


from . import route

