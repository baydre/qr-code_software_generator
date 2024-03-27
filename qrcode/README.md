# Running the Flask Application

This Flask application allows users to upload an image and generate a QR code from the image URL. Here's how to run it:

## Prerequisites

- Python 3.6 or higher
- Flask
- flask-SQLAlchemy
- Pillow
- qrcode
- flask_sqlalchemy
- werkzeug

You can install the necessary packages using pip:

```bash
pip install flask flask-sqlalchemy werkzeug pillow qrcode
```

## Steps to Run the Application

1. **Clone the repository or download the source code.**

2. **Navigate to the project directory.** Open a terminal and navigate to the directory where the source code is located.

3. **Set the Flask application environment variable.** This tells Flask where to find the application.

```bash
export FLASK_APP=app.py # Use 'set' instead of 'export' if you're on Windows
```

4. **Run the Flask application.** Use the `flask run` command to start the server.

```bash
flask run
```

The application will start running on `http://127.0.0.1:5000/`.

## API Endpoints

- **Upload an image:** Send a POST request to `http://127.0.0.1:5000/upload` with the image file in the form data. The server will return a JSON response with the image URL.

- **Generate a QR code:** Send a POST request to `http://127.0.0.1:5000/api/qrcode` with a JSON body containing the `image_url` parameter. The server will return a JSON response with the QR code link.

## Note

This application does not come with a front-end. You can use tools like curl or Postman to send requests to the server.Sure, here's how you can use `curl` to interact with the API:

## curl

1. **Upload an image:**

To upload an image, you can use the `-F` option in `curl` which lets you upload multipart form data. Replace `path_to_your_image` with the actual path to your image file.

```bash
curl -X POST -F "file=@C:/Users/HP/Pictures/Saved Pictures/beach1.jpg" http://127.0.0.1:5000/upload
```

The server will return a JSON response with the image URL.

2. **Generate a QR code:**

To generate a QR code, you need to send a POST request with a JSON body containing the `image_url` parameter. Replace `your_image_url` with the actual image URL you received from the upload endpoint.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"image_url":"http://localhost:5000/static/242fb168-19d7-4209-bce4-68e66bf843ec.jpg"}' http://127.0.0.1:5000/api/qrcode
```

The server will return a JSON response with the QR code link.

Remember to replace `path_to_your_image` and `your_image_url` with your actual image path and URL respectively.


## Thank you
