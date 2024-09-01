from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .database import db
from .models import User


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            access_token = create_access_token(identity=user.id)
            session['access_token'] = access_token
            return redirect(url_for('views.home'))
        return redirect(url_for('auth.login'))
    return render_template('auth.html')

@auth.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('login'))