import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

BACKEND_DIR = Path(__file__).parent.parent
CREDENTIALS_FILE = BACKEND_DIR / 'credentials.json'
TOKEN_FILE = BACKEND_DIR / 'token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_stored_credentials() -> Credentials | None:
    creds = None
    if TOKEN_FILE.exists():
        try:
            with open(TOKEN_FILE, 'r') as f:
                creds_data = json.load(f)
                creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
        except Exception:
            # Corrupted token, delete it
            TOKEN_FILE.unlink(missing_ok=True)
            return None
            
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            save_credentials(creds)
        except Exception:
            return None
            
    return creds

def save_credentials(credentials: Credentials):
    creds_data = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    with open(TOKEN_FILE, 'w') as f:
        json.dump(creds_data, f)
