# ventas_app/app/routes/purchase.py
from flask import Blueprint, request, redirect, url_for, flash, render_template
from app.models import Purchase, PurchaseItem, Product, User
from app import db

purchase = Blueprint('purchase', __name__)

@purchase.route('/purchase', methods=['POST'])
def make_purchase():
    user_id = request.form['user_id']
    products = request.form.getlist('product_id')
    quantities = request.form.getlist('quantity')
    
    purchase = Purchase(user_id=user_id, total=0)
    db.session.add(purchase)
    
    for product_id, quantity in zip(products, quantities):
        product = Product.query.get(product_id)
        if product.stock < int(quantity):
            flash('Compra no exitosa: Stock insuficiente', 'error')
            return redirect(url_for('main.index'))
        
        purchase_item = PurchaseItem(purchase=purchase, product_id=product_id, quantity=quantity)
        db.session.add(purchase_item)
        product.stock -= int(quantity)
        purchase.total += product.price * int(quantity)
    
    db.session.commit()
    flash('Compra exitosa', 'success')
    return redirect(url_for('purchase.purchase_history', user_id=user_id))

@purchase.route('/purchase_history/<int:user_id>')
def purchase_history(user_id):
    user = User.query.get_or_404(user_id)
    purchases = Purchase.query.filter_by(user_id=user_id).order_by(Purchase.date.desc()).all()
    return render_template('purchase_history.html', user=user, purchases=purchases)