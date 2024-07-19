from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models import Product
from app import db

product = Blueprint('product', __name__)

@product.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            name = request.form['name']
            price = float(request.form['price'])
            stock = int(request.form['stock'])
            
            current_app.logger.info(f"Intentando agregar producto: {name}, precio: {price}, stock: {stock}")
            
            new_product = Product(name=name, price=price, stock=stock)
            db.session.add(new_product)
            db.session.commit()
            
            current_app.logger.info(f"Producto agregado exitosamente: {new_product.id}")
            flash('Producto agregado exitosamente', 'success')
        except ValueError as ve:
            current_app.logger.error(f"Error de valor al agregar producto: {str(ve)}")
            flash('Error en los datos ingresados. Asegúrate de que el precio y el stock sean números válidos.', 'error')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al agregar producto: {str(e)}")
            flash(f'Error al agregar el producto: {str(e)}', 'error')
        
        return redirect(url_for('main.index'))
    
    return render_template('add_product.html')

@product.route('/increase_stock/<int:product_id>', methods=['POST'])
def increase_stock(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        amount = int(request.form['amount'])
        product.increase_stock(amount)
        db.session.commit()
        current_app.logger.info(f"Stock aumentado para producto {product_id}: +{amount}")
        flash('Stock aumentado exitosamente', 'success')
    except ValueError as ve:
        current_app.logger.error(f"Error de valor al aumentar stock: {str(ve)}")
        flash('Error en la cantidad ingresada. Debe ser un número entero.', 'error')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al aumentar stock: {str(e)}")
        flash(f'Error al aumentar el stock: {str(e)}', 'error')
    return redirect(url_for('main.index'))