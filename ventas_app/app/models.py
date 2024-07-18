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