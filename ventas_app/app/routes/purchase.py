
from flask import Blueprint, request, redirect, url_for, flash, render_template, current_app
from app.models import Purchase, PurchaseItem, Product, User
from app import db

purchase = Blueprint('purchase', __name__)

@purchase.route('/make_purchase', methods=['POST'])
def make_purchase():
    try:
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
        current_app.logger.info(f"Venta realizada: Productos {products}, Cantidades {quantities}")
        flash('Compra exitosa', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al realizar la compra: {str(e)}")
        flash(f'Error al realizar la compra: {str(e)}', 'error')
    
    return redirect(url_for('main.index'))

@purchase.route('/purchase_history/<int:user_id>')
def purchase_history(user_id):
    try:
        user = User.query.get_or_404(user_id)
        purchases = Purchase.query.filter_by(user_id=user_id).order_by(Purchase.date.desc()).all()
        return render_template('purchase_history.html', user=user, purchases=purchases)
    except Exception as e:
        current_app.logger.error(f"Error al recuperar el historial de compras: {str(e)}")
        flash('Error al cargar el historial de compras', 'error')
        return render_template('purchase_history.html', user=None, purchases=[])