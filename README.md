# Aplicaci-n-de-Gesti-n-de-Ventas
Aplicación web simple de gestión de ventas utilizando Python con el framework Flask para el backend, y HTML, CSS, y JavaScript

# Proyecto: Aplicación de Gestión de Ventas

## Estructura del Proyecto

```
ventas_app/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── add_product.html
│       └── sales.html
│
├── config.py
├── run.py
└── requirements.txt
```

## Pasos de Desarrollo (usando Scrum)

### Sprint 1: Configuración y Funcionalidades Básicas

1. Configuración del Proyecto
   - Crear la estructura de directorios
   - Configurar el entorno virtual
   - Instalar dependencias

2. Implementar Modelo de Datos
   - Crear modelos para Producto y Venta

3. Crear Rutas Básicas
   - Implementar ruta para la página principal
   - Implementar ruta para agregar productos

4. Diseñar Interfaz de Usuario Básica
   - Crear plantilla base
   - Crear página principal
   - Crear formulario para agregar productos

### Sprint 2: Funcionalidades de Ventas y Mejoras

1. Implementar Funcionalidad de Ventas
   - Crear ruta para registrar ventas
   - Diseñar interfaz para registrar ventas

2. Implementar Listado de Ventas
   - Crear ruta para ver el historial de ventas
   - Diseñar interfaz para mostrar el historial

3. Mejorar la Interfaz de Usuario
   - Agregar estilos CSS
   - Implementar validaciones en el frontend

4. Pruebas y Depuración
   - Realizar pruebas de todas las funcionalidades
   - Corregir errores encontrados

## Código

### config.py

```python
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'tu_clave_secreta_aqui'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### run.py

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

### app/__init__.py

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app import routes
    app.register_blueprint(routes.main)

    with app.app_context():
        db.create_all()

    return app
```

### app/models.py

```python
from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    product = db.relationship('Product', backref=db.backref('sales', lazy=True))
```

### app/routes.py

```python
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
```

### app/templates/base.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Aplicación de Ventas{% endblock %}</title>
    <style>
        /* Estilos básicos aquí */
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
        nav { margin-bottom: 20px; }
        nav a { margin-right: 10px; }
        .flash { padding: 10px; margin-bottom: 10px; border-radius: 5px; }
        .success { background-color: #d4edda; color: #155724; }
        .error { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <nav>
        <a href="{{ url_for('main.index') }}">Inicio</a>
        <a href="{{ url_for('main.add_product') }}">Agregar Producto</a>
        <a href="{{ url_for('main.sales') }}">Ventas</a>
    </nav>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="flash {{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    {% block content %}
    {% endblock %}
</body>
</html>
```

### app/templates/index.html

```html
{% extends "base.html" %}

{% block content %}
<h1>Productos Disponibles</h1>
<table>
    <thead>
        <tr>
            <th>Nombre</th>
            <th>Precio</th>
            <th>Stock</th>
            <th>Acción</th>
        </tr>
    </thead>
    <tbody>
        {% for product in products %}
        <tr>
            <td>{{ product.name }}</td>
            <td>${{ "%.2f"|format(product.price) }}</td>
            <td>{{ product.stock }}</td>
            <td>
                <form action="{{ url_for('main.register_sale') }}" method="post">
                    <input type="hidden" name="product_id" value="{{ product.id }}">
                    <input type="number" name="quantity" min="1" max="{{ product.stock }}" required>
                    <button type="submit">Vender</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

### app/templates/add_product.html

```html
{% extends "base.html" %}

{% block content %}
<h1>Agregar Nuevo Producto</h1>
<form method="post">
    <div>
        <label for="name">Nombre:</label>
        <input type="text" id="name" name="name" required>
    </div>
    <div>
        <label for="price">Precio:</label>
        <input type="number" id="price" name="price" step="0.01" min="0" required>
    </div>
    <div>
        <label for="stock">Stock:</label>
        <input type="number" id="stock" name="stock" min="0" required>
    </div>
    <button type="submit">Agregar Producto</button>
</form>
{% endblock %}
```

### app/templates/sales.html

```html
{% extends "base.html" %}

{% block content %}
<h1>Historial de Ventas</h1>
<table>
    <thead>
        <tr>
            <th>Fecha</th>
            <th>Producto</th>
            <th>Cantidad</th>
            <th>Precio Total</th>
        </tr>
    </thead>
    <tbody>
        {% for sale in sales %}
        <tr>
            <td>{{ sale.date.strftime('%Y-%m-%d %H:%M:%S') }}</td>
            <td>{{ sale.product.name }}</td>
            <td>{{ sale.quantity }}</td>
            <td>${{ "%.2f"|format(sale.total_price) }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

### requirements.txt

```
Flask==2.0.1
Flask-SQLAlchemy==2.5.1
```

# Instrucciones para ejecutar la Aplicación de Ventas

## Requisitos previos

- Python 3.7 o superior instalado en tu sistema
- pip (el gestor de paquetes de Python)
- Git (opcional, pero útil para clonar el repositorio si lo tienes en un control de versiones)

## Pasos para ejecutar la aplicación

1. Preparar el entorno de desarrollo:

   a. Abre una terminal o línea de comandos.
   
   b. Navega al directorio donde quieres crear el proyecto:
      ```
      cd ruta/a/tu/directorio
      ```

   c. Crea un nuevo directorio para el proyecto y navega a él:
      ```
      mkdir ventas_app
      cd ventas_app
      ```

2. Configurar un entorno virtual:

   a. Crea un nuevo entorno virtual:
      ```
      python -m venv venv
      ```

   b. Activa el entorno virtual:
      - En Windows:
        ```
        venv\Scripts\activate
        ```
      - En macOS/Linux:
        ```
        source venv/bin/activate
        ```

3. Instalar las dependencias:

   a. Crea un archivo `requirements.txt` con el siguiente contenido:
      ```
      Flask==2.0.1
      Flask-SQLAlchemy==2.5.1
      ```

   b. Instala las dependencias:
      ```
      pip install -r requirements.txt
      ```

4. Crear la estructura del proyecto:

   Crea los siguientes directorios y archivos según la estructura proporcionada anteriormente:
   ```
   ventas_app/
   │
   ├── app/
   │   ├── __init__.py
   │   ├── models.py
   │   ├── routes.py
   │   └── templates/
   │       ├── base.html
   │       ├── index.html
   │       ├── add_product.html
   │       └── sales.html
   │
   ├── config.py
   ├── run.py
   └── requirements.txt
   ```

5. Copiar el código:

   Copia el código proporcionado anteriormente en cada uno de los archivos correspondientes.

6. Ejecutar la aplicación:

   a. En la terminal, asegúrate de que el entorno virtual está activado.
   
   b. Ejecuta el siguiente comando:
      ```
      python run.py
      ```

7. Acceder a la aplicación:

   Abre un navegador web y visita `http://localhost:5000`

## Notas adicionales

- Si encuentras algún error relacionado con módulos no encontrados, asegúrate de que estás en el directorio correcto y que el entorno virtual está activado.
- Para detener la aplicación, presiona Ctrl+C en la terminal donde se está ejecutando.
- Cada vez que quieras ejecutar la aplicación, asegúrate de activar el entorno virtual primero.
