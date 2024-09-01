#!/usr/bin/env python
"""
KSUBEB QR Code Generator home page route.
"""
from flask import Blueprint, render_template, request, send_file\
    , redirect, url_for
from flask_login import login_required, current_user
from io import BytesIO
from .models import QRCode
from .database import db


views = Blueprint('views', __name__, url_prefix='/views')

@views.route('/', methods=['GET'])
def home():
    return render_template('home.html', user=current_user)
    #return 'Welcome to KSUBEB STAFF DATA BASE!'

# Define the route to view the database entries
@views.route('/database', methods=['GET'])
@login_required
def staff_records():
    # Query the database to fetch all entries
    entries = QRCode.query.all()
    
    # Pass the fetched entries to the Jinja template for rendering
    return render_template('database.html', entries=entries)

# search & filter staff records using staff ID as keyword
@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    entries = []

    if request.method == 'POST':
        search_term = request.form['search']
        search_pattern = f"%{search_term}%"
        entries = QRCode.query.filter(QRCode.file_number.like(search_pattern)).all()

    return render_template('database.html', user=current_user, entries=entries)

# Download Records from database Route
@views.route('/download_records/<file_number>', methods=['GET'])
@login_required
def download_records(file_number):
  """Download a single file based on the file_number."""
  record = QRCode.query.filter_by(file_number=file_number).first()

  if not record:
    return "File not found", 404

  # image to download 
  image_data = record.qr_img  # Retrieve the image data from the database
  image_name = record.file_number  # Use file_number for download name

  return send_file(BytesIO(image_data),
                   mimetype='image/png',  # png image format
                   as_attachment=True,
                   download_name=f"{image_name}.png")

# Delete Records from database Route
@views.route('/delete_records/<id>', methods=['GET'])
@login_required
def delete_records(id):
    """Delete records associated with a given ID."""
    records = QRCode.query.filter_by(id=id).all()
    for record in records:
        db.session.delete(record)
        db.session.commit()
        return redirect(url_for('views.staff_records'))
    return render_template('database.html', user=current_user)