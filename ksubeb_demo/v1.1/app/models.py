#!/usr/bin/env python3
"""
"""
from .database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)


class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_number = db.Column(db.Integer, nullable=False)
    qr_img = db.Column(db.LargeBinary, nullable=False)