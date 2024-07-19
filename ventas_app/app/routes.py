from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Product, User, Purchase, PurchaseItem

main = Blueprint('main', __name__)

@main.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        
        new_product = Product(name=name, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        
        flash('Producto agregado exitosamente', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('add_product.html')

@main.route('/increase_stock/<int:product_id>', methods=['POST'])
def increase_stock(product_id):
    product = Product.query.get_or_404(product_id)
    amount = int(request.form['amount'])
    product.increase_stock(amount)
    db.session.commit()
    flash('Stock aumentado exitosamente', 'success')
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('main.index'))
    return render_template('register.html')

@main.route('/purchase', methods=['POST'])
def make_purchase():
    user_id = request.form['user_id']
    products = request.form.getlist('product_id')
    quantities = request.form.getlist('quantity')
    
    purchase = Purchase(user_id=user_id, total=0)
    db.session.add(purchase)
    
    for product_id, quantity in zip(products, quantities):
        product = Product.query.get(product_id)
        quantity = int(quantity)
        if product.stock < quantity:
            flash('Compra no exitosa: Stock insuficiente', 'error')
            return redirect(url_for('main.index'))
        
        purchase_item = PurchaseItem(purchase=purchase, product_id=product_id, quantity=quantity)
        db.session.add(purchase_item)
        product.stock -= quantity
        purchase.total += product.price * quantity
    
    db.session.commit()
    flash('Compra exitosa', 'success')
    return redirect(url_for('main.purchase_history', user_id=user_id))

@main.route('/purchase_history/<int:user_id>')
def purchase_history(user_id):
    user = User.query.get_or_404(user_id)
    purchases = Purchase.query.filter_by(user_id=user_id).order_by(Purchase.date.desc()).all()
    return render_template('purchase_history.html', user=user, purchases=purchases)

@main.route('/sales')
def sales():
    purchases = Purchase.query.order_by(Purchase.date.desc()).all()
    return render_template('sales.html', sales=purchases)
