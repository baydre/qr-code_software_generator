#!/usr/bin/env python3
"""
model tables for the database.
QRCode table has id, staffname, and filename columns.
IDCard table has id, img, name, and mimetype columns.
User table has id, public_id, email, password, and super_admin columns.
"""
from .database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, default=False)

class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staffname = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    # qr = db.Column(db.LargeBinary, nullable=False)
    
class IDCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)