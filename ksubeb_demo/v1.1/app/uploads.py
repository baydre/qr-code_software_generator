#!/usr/bin/env python3
"""
"""
from io import BytesIO
import os, pyqrcode
from flask import Blueprint, request, flash, redirect, url_for, \
    send_file, render_template
from werkzeug.utils import secure_filename
# from flask import app
from .database import db
from .models import QRCode


uploads = Blueprint('uploads', __name__, url_prefix='/uploads')

# allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')


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

        # create folder if does not exist
        if file:
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # is the file present and in the right format?
        if file and allowed_file(file.filename):
            # collect and save user data to upload directory
            file_number = request.form['file_number']
            filename = secure_filename(file.filename)
            id_qr = secure_filename(file_number)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            # generate QRCode base on user data
            url = request.host_url + UPLOAD_FOLDER + filename
            qr = pyqrcode.create(url)
            qr_img_path = os.path.join(UPLOAD_FOLDER, id_qr)
            qr.png(qr_img_path, scale=8)

            # add generated data to QR table in the database
            qr_code = QRCode(staffname=file_number, filename=filename)
            db.session.add(qr_code)
            db.session.commit()

            return redirect(url_for('uploads.show_qr', name=id_qr))
    
    return render_template('upload.html')


# display QRCode function route
@uploads.route('/uploads/<name>', methods=['GET', 'POST'])
def show_qr(file_number):
    # display the QRCode image
    if request.method == 'POST':
        image = QRCode.query.filter_by(file_number).first()
        if not image:
            return 'QRCode not found'
        else:
            return send_file(BytesIO(image.qr_code), attachment_filename=image.file_number, as_attachment=False)

    return render_template('download.html')


# download QRCode route
@uploads.route('/download/<name>')
def download_image(file_number):
    image = QRCode.query.get(file_number)
    return send_file(BytesIO(image.qr_code), attachment_filename=image.file_number, as_attachment=True)