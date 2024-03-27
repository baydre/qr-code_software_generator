#!/usr/bin/env python3
"""
"""
from . import db


class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staffname = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)

    # def __repr__(self):
    #     return f"Staff('{self.staffname}', '{self.filename}')"