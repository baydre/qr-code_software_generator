#!/usr/bin/env python3
"""
database initialization module.
"""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# initialize the database
def db_init(app):
    db.init_app(app)