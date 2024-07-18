import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = 'tu_clave_secreta_aqui'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False