import json
import http.cookiejar
import os
import requests
from config.config import Config

def download_file_from_google_drive(file_id=Config.DEFAULT_FILE_ID, filename=Config.DEFAULT_FILENAME):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    destination = os.path.join(os.getcwd(), filename)
    save_response_content(response, destination)
    return destination

def download_file_from_google_drive_token(file_id=Config.DEFAULT_FILE_ID, filename=Config.OAUTH_TOKEN_FILE_PATH):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    destination = os.path.join(os.getcwd(), filename)
    save_response_content(response, destination)
    return destination

def download_creds(creds_file_id=Config.FILE_ID, creds_filename=Config.GOOGLE_CREDENTIALS_PATH):
    return download_file_from_google_drive(file_id=creds_file_id, filename=creds_filename)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

def convert_cookies_to_ytdlp_format(json_path='cookies.json', output_path='cookies.txt'):
    with open(json_path, 'r') as f:
        cookies = json.load(f)
    
    cookie_jar = http.cookiejar.MozillaCookieJar(output_path)
    
    for cookie_data in cookies:
        expires = int(cookie_data['expirationDate']) if not cookie_data.get('session', False) else None
        cookie = http.cookiejar.Cookie(
            version=0,
            name=cookie_data['name'],
            value=cookie_data['value'],
            port=None,
            port_specified=False,
            domain=cookie_data['domain'],
            domain_specified=True,
            domain_initial_dot=cookie_data['domain'].startswith('.'),
            path=cookie_data['path'],
            path_specified=bool(cookie_data['path']),
            secure=cookie_data['secure'],
            expires=expires,
            discard=False,
            comment=None,
            comment_url=None,
            rest={'HttpOnly': cookie_data['httpOnly']},
            rfc2109=False
        )
        cookie_jar.set_cookie(cookie)
    
    cookie_jar.save(ignore_discard=True, ignore_expires=True)
    return output_path
