from market import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=20), unique=True, nullable=False)
    email = db.Column(db.String(length=30), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    buget = db.Column(db.Float, default=1000)
    item = db.relationship('Item', backref='user', lazy=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=20), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    barcode = db.Column(db.String(length=12), unique=True, nullable=False)
    description = db.Column(db.String(length=1024), unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
