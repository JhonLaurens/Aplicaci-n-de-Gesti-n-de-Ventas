import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configurar logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    db.init_app(app)

    from .routes.main import main as main_blueprint
    from .routes.product import product as product_blueprint
    from .routes.purchase import purchase as purchase_blueprint
    from .routes.auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(purchase_blueprint)
    app.register_blueprint(auth_blueprint)

    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Base de datos inicializada correctamente")
        except Exception as e:
            app.logger.error(f"Error al inicializar la base de datos: {str(e)}")

    return app