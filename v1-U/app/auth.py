from flask import Blueprint, render_template, request, redirect, url_for, session\
, flash
from flask_login import login_user, logout_user, LoginManager, login_required\
, current_user
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from .database import db
from .models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password1']
        password_confirm = request.form['password2']

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Profile already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('username must be greater than 1 character.', category='error')
        # Check if passwords match
        elif password != password_confirm:
            flash('Passwords do not match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='danger')
        else:
        # hash passwords
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        # Create a new user and add them to the database
            new_user = User(email=email, username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Profile successfully created, Please log in.', category='success')
            return redirect(url_for('auth.login'))

    return render_template('sign_up.html', user=current_user)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            access_token = create_access_token(identity=user.id)
            session['access_token'] = access_token
            flash('Logged in successfully.', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Invalid username or password.', category='danger')
        return redirect(url_for('auth.login'))
    return render_template('auth.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', category='success')
    session.pop('access_token', None)
    return redirect(url_for('auth.login'))