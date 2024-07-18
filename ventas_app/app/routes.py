from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Product, Sale

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

@main.route('/register_sale', methods=['POST'])
def register_sale():
	product_id = int(request.form['product_id'])
	quantity = int(request.form['quantity'])
	
	product = Product.query.get_or_404(product_id)
	
	if product.stock < quantity:
		flash('No hay suficiente stock', 'error')
		return redirect(url_for('main.index'))
	
	total_price = product.price * quantity
	
	new_sale = Sale(product_id=product_id, quantity=quantity, total_price=total_price)
	product.stock -= quantity
	
	db.session.add(new_sale)
	db.session.commit()
	
	flash('Venta registrada exitosamente', 'success')
	return redirect(url_for('main.index'))

@main.route('/sales')
def sales():
	sales = Sale.query.order_by(Sale.date.desc()).all()
	return render_template('sales.html', sales=sales)