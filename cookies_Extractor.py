import os
import requests

DEFAULT_FILE_ID = '18tMZ36WoVNOA-JvdGgFhq4cYdqsMU66Q'
DEFAULT_FILENAME = 'cookies.json'

# FILE_ID='1GPLMy-9aQoNHRGbPuL2CENaHaCZpUgZZ'
FILE_ID='1rBx3pYheJ82VjzRkdgJpOXGWrKvC4OiW'
FILENAME2='credentials.json'

def download_file_from_google_drive(file_id=DEFAULT_FILE_ID, filename=DEFAULT_FILENAME):
    """
    Downloads a file from Google Drive and saves it in the current working directory.

    :param file_id: The unique identifier of the file on Google Drive.
    :param filename: The name to save the file as.
    """
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    # Get the current working directory
    current_directory = os.getcwd()

    # Construct the full path for the destination file
    destination = os.path.join(current_directory, filename)

    save_response_content(response, destination)
    return destination

def download_creds(creds_file_id=FILE_ID, creds_filename=FILENAME2):
   return  download_file_from_google_drive(file_id=creds_file_id, filename=creds_filename)

def get_confirm_token(response):
    """
    Retrieves the confirmation token from the response cookies if present.

    :param response: The response object from the initial request.
    :return: The confirmation token if found, else None.
    """
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    """
    Saves the content of the response to the specified destination file.

    :param response: The response object containing the file content.
    :param destination: The path where the file should be saved.
    """
    CHUNK_SIZE = 32768  # 32KB

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # Filter out keep-alive new chunks
                f.write(chunk)
