from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json
import os

def get_drive():
    gauth = GoogleAuth()
    gauth.LoadServiceConfigFile("client_secrets.json")
    gauth.ServiceAuth()
    return GoogleDrive(gauth)
