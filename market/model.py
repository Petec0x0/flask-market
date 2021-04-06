from market import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=20), unique=True, nullable=False)
    email = db.Column(db.String(length=30), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    buget = db.Column(db.Float, default=1000)
    item = db.relationship('Item', backref='user', lazy=True)
    
    def can_buy_item(self, item):
        """ 
        This method checks if user can afford a particular item
        
        Usage:
        >>> user.can_buy_item(item)
        
        returns True or False
        """
        return self.buget >= item.price
    
    def can_buy_sell(self, item):
        """ 
        This method checks if user have ownership to a particular item
        
        Usage:
        >>> user.can_buy_sell(item)
        
        returns True or False
        """
        return item in self.item
        


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=20), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    barcode = db.Column(db.String(length=12), unique=True, nullable=False)
    description = db.Column(db.String(length=1024), unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    def buy(self, user):
        self.owner_id = user.id
        user.buget -= self.price
        
        db.session.commit()
        
    def sell(self, user):
        self.owner_id = None
        user.buget += self.price
        
        db.session.commit()
