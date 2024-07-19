# ventas_app/app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('main.index'))
    return render_template('register.html')