#!/usr/bin/env python3
"""
database models.
"""
from .database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(128))
    qrcodes = db.relationship('QRCode', backref='owner', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)
    
    @property
    def is_authenticated(self):
        return True

class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_number = db.Column(db.String(50), nullable=False)
    local_govt = db.Column(db.String(50), nullable=False)
    id_img = db.Column(db.LargeBinary, nullable=False)
    qr_img = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))