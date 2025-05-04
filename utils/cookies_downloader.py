import requests
import os
from config import config

class GoogleDriveDownloader:
    def __init__(self):
        self.base_url = "https://docs.google.com/uc?export=download"
        
    def download(self, file_id=config.DEFAULT_FILE_ID, filename=config.DEFAULT_FILENAME):
        session = requests.Session()
        response = session.get(self.base_url, params={'id': file_id}, stream=True)
        token = self._get_confirm_token(response)
        
        if token:
            params = {'id': file_id, 'confirm': token}
            response = session.get(self.base_url, params=params, stream=True)
            
        with open(filename, "wb") as f:
            for chunk in response.iter_content(32768):
                if chunk:
                    f.write(chunk)
        return os.path.abspath(filename)
    
    def _get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None
