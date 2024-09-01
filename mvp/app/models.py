#!/usr/bin/env python3
"""
database models.
"""
from .database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)


class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_number = db.Column(db.String(50), nullable=False)
    local_govt = db.Column(db.String(50), nullable=False)
    id_img = db.Column(db.LargeBinary, nullable=False)
    qr_img = db.Column(db.LargeBinary, nullable=False)