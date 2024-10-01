# undecided

## Getting Started
- Run the command below in your terminal to install app requirement:

    `pip install -r requirements.txt`

- Next, activate your create and activate your virtual environment:

    `python3 -m venv [venv-name]`

    `source [venv-name]/bin/activate`

## Google Drive API Storage Setup

1. Install Google Drive API Client Libraries. Ensure you have the necessary libraries installed:

     `pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2`

1. Service Account Authentication:
You will need a service_account.json file to authenticate the requests to Google Drive.

1. Modify Flask App:
We need to integrate file uploading into the Google Drive backup flow. We’ll modify the file upload process so that after the file is uploaded in Flask, it gets backed up to Google Drive.