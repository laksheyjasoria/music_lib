import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from config import GOOGLE_CREDENTIALS_PATH, DRIVE_FILE_ID

class GoogleDriveManager:
    """
    Secure Google Drive integration class using configuration parameters
    
    Features:
    - No token.json storage
    - Service account or OAuth client authentication
    - Configurable via external config.py
    """
    
    def __init__(self):
        self.service = self._authenticate()
        self.default_file_id = DRIVE_FILE_ID

    def _authenticate(self):
        """Flexible authentication supporting both service accounts and OAuth clients"""
        try:
            # Try service account first
            creds = service_account.Credentials.from_service_account_file(
                GOOGLE_CREDENTIALS_PATH,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
        except ValueError:
            # Fall back to OAuth client if service account fails
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_CREDENTIALS_PATH,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
            creds = flow.run_local_server(port=0)
            
        return build('drive', 'v3', credentials=creds)

    def get_file_content(self, file_id=None):
        """
        Retrieve file content from Google Drive
        :param file_id: Uses config default if not specified
        :return: File content as bytes
        """
        target_id = file_id or self.default_file_id
        try:
            request = self.service.files().get_media(fileId=target_id)
            return request.execute()
        except Exception as e:
            raise DriveIntegrationError(f"File fetch failed: {str(e)}")

    def update_file_content(self, content, mime_type, file_id=None):
        """
        Update file content on Google Drive
        :param content: Bytes-like object
        :param mime_type: File MIME type
        :param file_id: Uses config default if not specified
        :return: Updated file metadata
        """
        target_id = file_id or self.default_file_id
        try:
            media = MediaIoBaseUpload(
                io.BytesIO(content),
                mimetype=mime_type,
                resumable=True
            )
            return self.service.files().update(
                fileId=target_id,
                media_body=media
            ).execute()
        except Exception as e:
            raise DriveIntegrationError(f"File update failed: {str(e)}")

class DriveIntegrationError(Exception):
    """Custom exception for drive operations"""
    pass

# Usage in another class
class YourApplicationClass:
    def __init__(self):
        self.drive = GoogleDriveManager()
        
    def process_file(self):
        try:
            # Get file content using config default ID
            content = self.drive.get_file_content()
            
            # Process content
            modified_content = content + b"\nProcessed by my app"
            
            # Update file using config default ID
            self.drive.update_file_content(
                modified_content,
                'text/plain'
            )
            
        except DriveIntegrationError as e:
            print(f"Drive error occurred: {str(e)}")
