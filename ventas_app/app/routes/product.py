# ventas_app/app/routes/product.py
from flask import Blueprint, request, redirect, url_for, flash
from app.models import Product
from app import db

product = Blueprint('product', __name__)

@product.route('/increase_stock/<int:product_id>', methods=['POST'])
def increase_stock(product_id):
	product = Product.query.get_or_404(product_id)
	amount = int(request.form['amount'])
	product.increase_stock(amount)
	db.session.commit()
	flash('Stock aumentado exitosamente', 'success')
	return redirect(url_for('main.index'))