from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import qrcode
import os
import uuid
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uploads.db'
db = SQLAlchemy(app)

class UploadedImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(200), nullable=False)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1].lower()
        image_path = os.path.join('static', unique_filename)

        file.save(image_path)

        with app.app_context():
            # Create the database tables
            db.create_all()

            # Save image path to the database
            new_image = UploadedImage(image_path=image_path)
            db.session.add(new_image)
            db.session.commit()

        return jsonify({'image_url': request.url_root + image_path}), 200
    
@app.route('/api/qrcode', methods=['POST'])
def generate_qrcode_api():
    if 'image_url' not in request.json:
        return jsonify({'error': 'Missing image_url parameter'}), 400

    image_url = request.json['image_url']
    qr_img = generate_qr_code(image_url)

    # Extract the filename from the image_url
    filename = os.path.basename(image_url)

    # Generate a new filename for the QR code by prepending a character
    qr_img_filename = 'q_' + filename

    qr_img_path = os.path.join('static', qr_img_filename)
    qr_img.save(qr_img_path)

    return jsonify({'qrcode_link': qr_img_path}), 200

if __name__ == '__main__':
    app.run(debug=True)
