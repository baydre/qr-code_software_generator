#!/usr/bin/env python3
"""
"""
from io import BytesIO
import os
import pyqrcode
from flask import Blueprint, request, flash, redirect, url_for, render_template, send_file, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .database import db
from .models import QRCode

uploads = Blueprint('uploads', __name__, url_prefix='/uploads')

# check if the file to uploaded is an image
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# image upload & QRCode generator route
@uploads.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # Ensure the UPLOAD_FOLDER directory exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

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
        if len(file.read()) > current_app.config['MAX_FILE_SIZE']:
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
            id_image_path = os.path.join(upload_folder, filename)
            file.save(id_image_path)

            # Read the file as bytes
            with open(id_image_path, 'rb') as f:
                id_img_bytes = f.read()

            # generate QRCode based on user data
            qr_url = url_for('uploads.uploaded_file', filename=filename, _external=True)
            qr = pyqrcode.create(qr_url)
            qr_img_path = os.path.join(upload_folder, f"{file_number}.png")
            qr.png(qr_img_path, scale=8)

            # Read the QR code as bytes
            with open(qr_img_path, 'rb') as f:
                qr_img_bytes = f.read()

            # add generated data to QR table in the database
            qr_code = QRCode(file_number=file_number, local_govt=local_govt, qr_img=qr_img_bytes, id_img=id_img_bytes)
            db.session.add(qr_code)
            db.session.commit()

            # return "QRCode generated successfully!"
            # Redirect to the display page with the file_number parameter
        return redirect(url_for('uploads.download_page', file_number=file_number))

    return render_template('upload.html', user=current_user)

# uploaded file route
@uploads.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_file(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

# download page
@uploads.route('/download')
@login_required
def download_page():
    # Get the file_number from the request or wherever you obtain it
    file_number = request.args.get('file_number')
    return render_template('download.html', file_number=file_number, user=current_user)

# display QRCode route
@uploads.route('/display/<file_number>', methods=['GET'])
@login_required
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
@login_required
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