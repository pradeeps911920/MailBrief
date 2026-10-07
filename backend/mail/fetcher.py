import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastapi import APIRouter, HTTPException
from auth.credentials import get_stored_credentials

router = APIRouter(prefix="/mail", tags=["mail"])

MAX_EMAIL_CHARS = 12000

def parse_email_body(payload: dict) -> str:
    """Recursively parses the email payload to extract the text/plain or text/html body."""
    body_content = ""
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                if data:
                    body_content += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            elif part['mimeType'] == 'text/html' and not body_content:
                # Fallback to HTML if plain text isn't found yet
                data = part['body'].get('data', '')
                if data:
                    import re
                    html = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    # Better HTML stripping
                    html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL)
                    html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL)
                    html = re.sub(r'<br\s*/?>', '\n', html)
                    html = re.sub(r'</p>', '\n\n', html)
                    text = re.sub(r'<[^>]+>', ' ', html)
                    # Clean up multiple spaces and empty lines
                    text = re.sub(r' {2,}', ' ', text)
                    body_content = re.sub(r'\n\s*\n', '\n\n', text).strip()
            elif 'parts' in part:
                # Recurse into nested parts (e.g. multipart/alternative)
                body_content += parse_email_body(part)
    elif 'body' in payload and 'data' in payload['body']:
        data = payload['body']['data']
        body_content = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

    return body_content

@router.get("/fetch")
def fetch_recent_emails(max_results: int = 50):
    """Fetches the most recent emails from the authenticated user's inbox."""
    creds = get_stored_credentials()
    if not creds:
        raise HTTPException(status_code=401, detail="Gmail not connected.")

    try:
        service = build('gmail', 'v1', credentials=creds)
        
        query = "newer_than:1d"
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])
        
        fetched_emails = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown Sender')
            date = next((h['value'] for h in headers if h['name'].lower() == 'date'), 'Unknown Date')
            
            full_body = parse_email_body(msg['payload'])
            
            # If parsing fails or it's empty, fallback to snippet
            if not full_body.strip():
                full_body = msg.get('snippet', '')
                
            if len(full_body) > MAX_EMAIL_CHARS:
                full_body = full_body[:MAX_EMAIL_CHARS] + "\n\n...[CONTENT TRUNCATED]..."
            
            fetched_emails.append({
                'id': msg['id'],
                'threadId': msg['threadId'],
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': full_body,
            })
            
        return fetched_emails
        
    except HttpError as error:
        raise HTTPException(status_code=502, detail="Gmail API error.")
