# ventas_app/app/routes/main.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ventas_app.app import db
from ventas_app.app.models import Product

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/sales')
def sales():
	return render_template('sales.html')

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