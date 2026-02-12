# app.py

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from models import db, User, Product
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Importing routes after creating the Flask app object
from routes import *

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Function to add products
def add_products():
    with app.app_context():
        # Add products to the database if the Product table is empty
        if not Product.query.first():
            products_data = [
                {'name': 'stray kids lightstick', 'price': 19.99, 'stock': 2, 'image_path': 'images/lightstick/skz-lightstick.jpg'},
                {'name': 'nct lightstick', 'price': 29.99, 'stock': 2, 'image_path': 'images/lightstick/nct-lightstick.jpg'},
                {'name': 'blackpink lightstick', 'price': 39.99, 'stock': 2, 'image_path': 'images/lightstick/blackpink-lightstick.jpg'},
                {'name': 'enhypen lightstick', 'price': 22.99, 'stock': 2, 'image_path': 'images/lightstick/rv-lightstick.jpg'},
                {'name': 'monsta x lightstick', 'price': 35.99, 'stock': 2, 'image_path': 'images/lightstick/monstax-lightstick.jpg'},
                {'name': 'the boyz lightstick', 'price': 24.99, 'stock': 2, 'image_path': 'images/lightstick/tbz-lightstick.jpg'},
            ]

            for product_info in products_data:
                new_product = Product(**product_info)
                db.session.add(new_product)

            db.session.commit()

# Run the product addition function if this script is executed directly
if __name__ == '__main__':
    with app.app_context():
        # Create or upgrade the database
        db.create_all()
        # Add products
        add_products()
    app.run(debug=True)