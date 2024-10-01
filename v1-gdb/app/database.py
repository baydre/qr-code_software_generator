#!/usr/bin/env python3
"""
database initialization module.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

# initialize the database
def db_init(app):
    db.init_app(app)
    migrate.init_app(app, db)