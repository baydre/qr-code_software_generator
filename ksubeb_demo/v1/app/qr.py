import os, pyqrcode
from flask import current_app as app
from flask import Blueprint, redirect, send_from_directory, request, url_for \
, render_template
from . import db
from .models import QRCode


qr = Blueprint('qr', __name__, url_prefix='/qr')

@qr.route('/qr', methods=['GET'])
def qr_page():
    return render_template('upload.html')
    #return 'KSUBEB STAFF QR CODE GENERATOR PAGE!'

@qr.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        username = request.form['username']
        filename = username + '.png'
        file_path = os.path.join(app, filename)
        file.save(file_path)

        # Generate QR code
        url = request.host_url + 'uploads/' + filename
        qr = pyqrcode.create(url)
        qr_img_path = os.path.join(app, filename)
        qr.png(qr_img_path, scale=8)

        # Save to database using SQLAlchemy
        qr_code = QRCode(staffname=username, filename=filename)
        db.session.add(qr_code)
        db.session.commit()

        return redirect(url_for('show_qr', staffname=username))

    return 'Error uploading file'

@qr.route('/show_qr/<username>')
def show_qr(username):
    return f'''
    <html>
    <head>
        <title>QR Code</title>
    </head>
    <body>
        <img src="/uploads/{username}.png" alt="QR Code">
        <br>
        <a href="/download/{username}" download>Download QR Code</a>
    </body>
    </html>
    '''

@qr.route('/download/<username>')
def download_qr(username):
    return send_from_directory(app, f'{username}.png', mimetype='image/png', as_attachment=True)