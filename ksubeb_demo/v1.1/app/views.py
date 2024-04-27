#!/usr/bin/env python
"""
KSUBEB QR Code Generator home page route.
"""
from flask import Blueprint, render_template
from .models import QRCode


views = Blueprint('views', __name__, url_prefix='/views')

@views.route('/', methods=['GET'])
def home():
    return render_template('home.html')
    #return 'Welcome to KSUBEB STAFF DATA BASE!'

# Define the route to view the database entries
@views.route('/database', methods=['GET'])
def staff_records():
    # Query the database to fetch all entries
    entries = QRCode.query.all()  # Replace YourModel with your actual database model
    
    # Pass the fetched entries to the Jinja template for rendering
    return render_template('database.html', entries=entries)