# models.py

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Create a many-to-many relationship table for the shopping cart
cart_product = db.Table('cart_product',
    db.Column('cart_id', db.Integer, db.ForeignKey('shopping_cart.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

purchase_history = db.Table(
    'purchase_history',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Add relationship
    purchased_products = db.relationship('Product', secondary=purchase_history, backref='purchasers')
    carts = db.relationship('ShoppingCart', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)

class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Define the relationship with the Product model
    products = db.relationship('Product', secondary=cart_product, backref='carts')

    def __repr__(self):
        return f"ShoppingCart(user_id={self.user_id}, products={self.products})"
