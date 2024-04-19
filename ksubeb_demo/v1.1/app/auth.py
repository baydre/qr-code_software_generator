#!/usr/bin/env python3
""""""
from flask import app
from flask import Blueprint, jsonify, render_template, make_response \
    , request, redirect, url_for
from flask_jwt_extended import create_access_token, get_jwt_identity \
    , jwt_required, set_access_cookies, unset_jwt_cookies
from datetime import datetime, timedelta, timezone
from .database import db
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash
import uuid

auth = Blueprint('auth', __name__, url_prefix='/auth')


# JWT refresh token function
@auth.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt_identity()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@auth.route('/user', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users': output})


@auth.route('/user/<public_id>', methods=['GET'])
@jwt_required()
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})
    
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


# create user route
@auth.route('/user', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    
    if 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = User(public_id=str(uuid.uuid4()), email=data['email'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


# login route
@auth.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(render_template('login.html'), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response(render_template('login.html'), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    if check_password_hash(user.password, auth.password):
        response = make_response(render_template('login_success.html'))
        access_token = create_access_token(identity=auth.username)
        set_access_cookies(response, access_token)
        return response
    
    return make_response(render_template('login.html'), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

# logout route
@auth.route('/logout')
def logout():
    response = make_response(redirect(url_for('auth.login')))
    unset_jwt_cookies(response)
    return response