from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

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
        db.create_all()

    return app