# ventas_app/app/routes/main.py
from flask import Blueprint, render_template, request

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
		# Aquí puedes manejar la lógica para agregar un producto
		# Por ejemplo, obtener datos del formulario:
		product_name = request.form.get('product_name')
		# Procesar y guardar el producto...
		return 'Producto agregado exitosamente'
	return render_template('add_product.html')