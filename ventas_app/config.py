import os
from dotenv import load_dotenv, find_dotenv

# Cargar variables de entorno desde .env file
dotenv_path = find_dotenv()
if dotenv_path:
    try:
        load_dotenv(dotenv_path)
    except UnicodeDecodeError as e:
        print(f"Error loading .env file: {e}")

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_muy_dificil_de_adivinar'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False