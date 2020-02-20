from flaskinventory import db
from datetime import datetime
from sqlalchemy.orm import relationship


class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Location(db.Model):
    db.__tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    loc_name = db.Column(db.String(20), unique=True, nullable=False)
    stocks = relationship("Stock", back_populates="location")

    def __repr__(self):
        return f"Location('{self.id}','{self.loc_name}')"
        return "Location('{self.loc_id}','{self.loc_name}')"


class Product(db.Model):
    db.__tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(20), unique=True, nullable=False)
    stocks = relationship("Stock", back_populates="product")

    def __repr__(self):
        return f"Product('{self.id}','{self.prod_name}','{self.prod_qty}')"


class Stock(db.Model):
    db.__tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = relationship('Product', back_populates="stocks")
    loc_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = relationship('Location', back_populates="stocks")
    sells = relationship('Sell', back_populates="stocks")
    price = db.Column(db.Integer, nullable=False)
    prod_qty = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Product('{self.id}')"


class Movement(db.Model):
    db.__tablename__ = 'move'
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, default=datetime.utcnow)
    frm = db.Column(db.String(20), nullable=False)
    to = db.Column(db.String(20), nullable=False)
    pname = db.Column(db.String(20), nullable=False)
    pqty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Movement('{self.id}','{self.ts}','{self.frm}','{self.to}','{self.pname}','{self.pqty}')"


class Balance(db.Model):
    db.__tablename__ = 'balance'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    product = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_unit = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Balance('{self.id}','{self.product}','{self.location}','{self.quantity}','{self.price_unit}')"


class Person(db.Model):
    db.__tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.String, nullable=True)
    code = db.Column(db.String, nullable=False)
    sells = relationship("Sell", back_populates="person")

    def __repr__(self):
        return f"Balance('{self.bid}','{self.product}','{self.location}','{self.quantity}')"


class Sell(db.Model):
    db.__tablename__ = 'sell'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    qty = db.Column(db.String(20), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = relationship('Person', back_populates="sells")
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    stocks = relationship('Stock', back_populates="sells")
    credit = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Sell('{self.id}','{self.product}','{self.location}','{self.quantity}')"
