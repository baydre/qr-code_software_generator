#!/usr/bin/env python
"""
KSUBEB QR Code Generator home page route.
"""
from flask import Blueprint, render_template, request
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

# search & filter staff records using staff ID as keyword
@views.route('/search', methods=['GET', 'POST'])
def search():
    entries = []

    if request.method == 'POST':
        search_term = request.form['search']
        search_pattern = f"%{search_term}%"
        entries = QRCode.query.filter(QRCode.file_number.like(search_pattern)).all()

    return render_template('database.html', entries=entries)

# Download Records from database Route
# @views.route('/download_records', methods=['POST'])
# def download_records():
    # selected_record_ids = request.json  # IDs of selected records sent from frontend
    # Retrieve data (e.g., file paths) corresponding to selected record IDs from the database
    # Perform any necessary processing (e.g., zipping files)
    # Send data back to the frontend for download
    # Example: return jsonify({'success': True, 'message': 'Records downloaded successfully'})

# Delete Records from database Route
# @views.route('/delete_records', methods=['POST'])
# def delete_records():
    # selected_record_ids = request.json  # IDs of selected records sent from frontend
    # Delete records corresponding to selected record IDs from the database
    # Example: db.session.query(Record).filter(Record.id.in_(selected_record_ids)).delete(synchronize_session=False)
    # Commit changes to the database
    # Example: db.session.commit()
    # Return a response indicating success or failure
    # Example: return jsonify({'success': True, 'message': 'Records deleted successfully'})