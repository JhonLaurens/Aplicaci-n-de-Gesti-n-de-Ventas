from flask import Blueprint, render_template, request, redirect, url_for, flash
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
            
            new_product = Product(name=name, price=price, stock=stock)
            db.session.add(new_product)
            db.session.commit()
            
            flash('Producto agregado exitosamente', 'success')
        except ValueError:
            flash('Error en los datos ingresados', 'error')
        except Exception as e:
            db.session.rollback()
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
        flash('Stock aumentado exitosamente', 'success')
    except ValueError:
        flash('Error en la cantidad ingresada', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al aumentar el stock: {str(e)}', 'error')
    return redirect(url_for('main.index'))