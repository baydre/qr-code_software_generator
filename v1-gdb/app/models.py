#!/usr/bin/env python3
"""
database models.
"""
from .database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    qrcodes = db.relationship('QRCode', backref='owner', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
  
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class QRCode(db.Model):
    __tablename__ = 'qrcode'

    id = db.Column(db.Integer, primary_key=True)
    file_number = db.Column(db.String(50), nullable=False)
    local_govt = db.Column(db.String(50), nullable=False)
    id_img = db.Column(db.LargeBinary, nullable=False)
    qr_img = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))