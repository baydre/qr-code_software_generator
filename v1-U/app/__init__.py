#!/usr/bin/env python
"""
"""
import os
from flask import Flask, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from datetime import timedelta
from .database import db_init
from .models import User

def create_app():
    """
    Create a Flask application.
    """
    app = Flask(__name__)
    CORS(app)

    UPLOAD_FOLDER = './uploads'

    app.config['SECRET_KEY'] = 'saabrisay'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ksubeb_id.sqlite3'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 # 1MB


    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_SECRET_KEY"] = "jwt-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["ALLOWED_EXTENSIONS"] = {'png', 'jpg', 'jpeg'}

    app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), 'uploads')
    app.config["MAX_FILE_SIZE"] = 1024 * 1024  # 1MB
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('auth.login'))
    
    JWTManager(app)
        

    # Initialize the database
    db_init(app)

    from .views import views
    from .auth import auth
    from .uploads import uploads

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(uploads, url_prefix='/')
    
    from .models import db
    # create tables if they do not exist
    with app.app_context():
        db.create_all()

    return app