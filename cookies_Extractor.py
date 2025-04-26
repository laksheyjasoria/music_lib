import os
import requests

def download_file_from_google_drive(file_id, filename=None):
    """
    Downloads a file from Google Drive and saves it in the current working directory.

    :param file_id: The unique identifier of the file on Google Drive.
    :param filename: Optional. The name to save the file as. If not provided, the file_id is used.
    """
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    # Determine the filename
    if not filename:
        filename = file_id  # Default to file_id if no filename is provided

    # Get the current working directory
    current_directory = os.getcwd()

    # Construct the full path for the destination file
    destination = os.path.join(current_directory, filename)

    save_response_content(response, destination)
    print(f"File downloaded successfully and saved as: {destination}")

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

# # Example usage
# if __name__ == "__main__":
#     file_id = 'YOUR_FILE_ID'  # Replace with your actual file ID
#     # Optionally, specify a filename. If not provided, file_id will be used as the filename.
#     download_file_from_google_drive(file_id, filename='desired_filename.ext')
