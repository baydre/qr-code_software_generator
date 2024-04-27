#!/usr/bin/env python3
"""
"""
from io import BytesIO
import os
import pyqrcode
from flask import Blueprint, request, flash, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from .database import db
from .models import QRCode

uploads = Blueprint('uploads', __name__, url_prefix='/uploads')

# allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Maximum file size allowed (1MB)
MAX_FILE_SIZE = 1024 * 1024  # 1MB


# check if the file to uploaded is an image
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# image upload & QRCode generator route
@uploads.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # check file size
        if len(file.read()) > MAX_FILE_SIZE:
            flash('File size exceeds maximum limit (1MB)')
            return redirect(request.url)
        file.seek(0)  # Reset file pointer to beginning after reading

        # is the file present and in the right format?
        if file and allowed_file(file.filename):
            # collect and save user data to upload directory
            file_number = request.form['file_number']
            local_govt = request.form['local_govt']
            
            # Save image file
            filename = secure_filename(file.filename)
            id_image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(id_image_path)

            # generate QRCode based on user data
            qr_url = request.host_url + 'uploads/' + filename
            qr = pyqrcode.create(qr_url)
            qr_img_path = os.path.join(UPLOAD_FOLDER, f"{file_number}.png")
            qr.png(qr_img_path, scale=8)

            # Read the generated QR code PNG file content
            with open(qr_img_path, 'rb') as f:
                qr_img_data = f.read()

            # add generated data to QR table in the database
            qr_code = QRCode(file_number=file_number, local_govt=local_govt, qr_img=qr_img_data)
            db.session.add(qr_code)
            db.session.commit()

            # return "QRCode generated successfully!"
            # Redirect to the display page with the file_number parameter
        return redirect(url_for('uploads.download_page', file_number=file_number))

    return render_template('upload.html')

# download page
@uploads.route('/download')
def download_page():
    # Get the file_number from the request or wherever you obtain it
    file_number = request.args.get('file_number')
    return render_template('download.html', file_number=file_number)

# display QRCode route
@uploads.route('/display/<file_number>', methods=['GET'])
def display(file_number):
    # Retrieve QR code data from the database based on file_number
    qr_code = QRCode.query.filter_by(file_number=file_number).first()
    if qr_code:
        # Serve the QR code image for display
        return send_file(BytesIO(qr_code.qr_img),
                         mimetype='image/png')
    else:
        # Handle case where QR code with given file_number is not found
        return "QR Code not found"

# download QRCode route
@uploads.route('/download/<file_number>', methods=['GET'])
def download(file_number):
    # Retrieve QR code data from the database based on file_number
    qr_code = QRCode.query.filter_by(file_number=file_number).first()
    if qr_code:
        # Serve the QR code image for download
        return send_file(BytesIO(qr_code.qr_img),
                         mimetype='image/png',
                         as_attachment=True,
                         download_name=f"{file_number}.png")
    else:
        # Handle case where QR code with given file_number is not found
        return "QR Code not found"