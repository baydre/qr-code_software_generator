#!/usr/bin/env python
"""
"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """
    Create a Flask application.
    """
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = 'saabrisay'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qr_codes.sqlite3'

    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from .views import views
    from .qr import qr

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(qr, url_prefix='/')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app