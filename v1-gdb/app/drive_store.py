#!/usr/bin/env python3
"""
Google Drive API Module.
"""
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

# Set the required scopes and service account credentials
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'baydre_serv_acct.json'  # json file actual path
PARENT_FOLDER_ID = '1w4T1A9V9zLRIX0yRHhtilkmP9bSYstp-'  # Drive folder ID

def authenticate():
    """
    Authenticates with Google Drive using the service account credentials.
    """
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def create_folder_if_not_exists(service, folder_name, parent_id):
    """
    Creates a folder in Google Drive if it doesn't already exist.

    :param service: The Google Drive API service instance.
    :param folder_name: Name of the folder to create.
    :param parent_id: ID of the parent folder where the new folder will be created.
    :return: The folder ID of the created or existing folder.
    """
    # Search for the folder to see if it already exists
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    if items:
        # Folder already exists, return the folder ID
        return items[0]['id']
    else:
        # Folder doesn't exist, create it
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')

def upload_to_drive(file_path, filename, foldername):
    """
    Uploads a file to a specified folder on Google Drive.
    
    :param file_path: Path to the file on the local system.
    :param filename: Name to give the file on Google Drive.
    :param foldername: Name of the folder on Google Drive to upload the file to.
    :return: File ID of the uploaded file on Google Drive.
    """
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # Check if the folder exists, and create it if not
    folder_id = create_folder_if_not_exists(service, foldername, PARENT_FOLDER_ID)

    # Prepare file metadata for uploading
    file_metadata = {
        'name': filename,
        'parents': [folder_id]  # Upload file to the specified folder
    }

    # Prepare the file to upload
    media = MediaFileUpload(file_path, resumable=True)

    # Upload the file to Google Drive
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return file.get('id')
