# routes.py

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from models import User, Product, ShoppingCart, cart_product
from utils import is_valid_password

@app.route('/')
def home():
    # Fetch products from the database
    products = Product.query.all()
    # Pass the products to the template
    return render_template('home.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        elif user is None:
            flash('Account does not exist.', 'danger')
        elif user.password != password:
            flash('Login failed. Wrong password', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Password and Confirm Password do not match.', 'danger')
        else:
            if User.query.filter_by(username=username).first():
                flash('Username already taken. Please choose another.', 'danger')
            elif not is_valid_password(password):
                flash('A minimum 8 characters password contains a combination of uppercase and lowercase letter and number are required.', 'danger')
            else:
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully! You can now login.', 'success')
                return redirect(url_for('signup'))

    return render_template('signup.html')


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)

    if product and product.stock > 0:
        product.stock -= 1

        # Check if the user already has a cart for this product, create one if not
        user_cart = ShoppingCart.query.filter_by(user_id=current_user.id).join(cart_product).filter(cart_product.c.product_id == product.id).first()

        if not user_cart:
            user_cart = ShoppingCart(user_id=current_user.id, quantity=1)
            user_cart.products.append(product)
            db.session.add(user_cart)
        else:
            # Check if the product is already in the cart
            existing_item = ShoppingCart.query.filter_by(user_id=current_user.id).join(cart_product).filter(cart_product.c.product_id == product.id, ShoppingCart.id == cart_product.c.cart_id).first()

            if existing_item:
                existing_item.quantity += 1
            else:
                user_cart.products.append(product)
                user_cart.quantity += 1  # Increment the cart quantity

        db.session.commit()
        flash(f'Added {product.name} to your cart!', 'success')
        return redirect(url_for('home'))
    else:
        flash(f'Sorry, {product.name} is out of stock!', 'danger')
        return redirect(url_for('home'))

# Updated view_cart route
@app.route('/cart')
@login_required
def view_cart():
    # Fetch the user's carts
    user_carts = current_user.carts

    # Create a list to store cart items (product, quantity) for rendering
    cart_items = []

    # Iterate through each shopping cart and extract product information
    for cart in user_carts:
        for product in cart.products:
            # Find the corresponding quantity for each product in the cart
            quantity = ShoppingCart.query.filter_by(user_id=current_user.id, id=cart.id).join(cart_product).filter(cart_product.c.product_id == product.id).first().quantity

            cart_items.append({'product': product, 'quantity': quantity})

    return render_template('cart.html', cart_items=cart_items)

@app.route('/cart_count')
@login_required
def get_cart_count():
    cart_count = current_user.carts.count()
    return {'cart_count': cart_count}

@app.route('/proceed_to_purchase', methods=['POST'])
@login_required
def proceed_to_purchase():
    # Get user's carts
    user_carts = current_user.carts

    if not user_carts:
        flash('Your cart is empty. Add items to your cart before proceeding to purchase.', 'warning')
    else:
        for cart in user_carts:
            for product in cart.products:
                if product.stock < cart.quantity:
                    flash(f'Not enough stock for {product.name}.', 'danger')
                    return redirect(url_for('view_cart'))

            # No need to explicitly update the user_id
            db.session.delete(cart)

        # Commit the changes after processing all carts
        db.session.commit()

        flash('Purchase completed! Thank you for shopping with us.', 'success')

    return redirect(url_for('view_cart'))

# Not being implemented
@app.route('/wishlist')
@login_required
def wishlist():
    return render_template('wishlist.html')