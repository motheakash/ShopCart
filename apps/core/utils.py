from rest_framework.pagination import PageNumberPagination
import os
import re
import base64
import json
import requests
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Dict
from config.settings.local import EMAIL_CREDS_FILE,EMAIL_CREDENTIALS_FILE, FROM_EMAIL



class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100 



class EmailSending:
    def __init__(self, credentials_file: str, token_file: str, from_email: str):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.from_email = from_email

    def get_gmail_service(self) -> build:
        """Gets the Gmail API service."""
        creds = None
        
        # Load credentials from token file
        if os.path.exists(self.token_file):
            try:
                creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
            except ValueError:
                # Token file is invalid or missing fields, trigger OAuth flow
                creds = None

        # If there are no valid credentials, go through the OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=8888)
                
                # Save the credentials for future use
                with open(self.token_file, 'w') as token:
                    token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def create_message(self, to: str, subject: str, message_text: str) -> Dict[str, str]:
        """Creates a message for an email."""
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = self.from_email
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw}

    def send_email(self, to: str, subject: str, message_text: str) -> None:
        """Send an email message."""
        service = self.get_gmail_service()
        message = self.create_message(to, subject, message_text)
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"Message sent: {sent_message['id']}")



def replace_numbers(text: str) -> str:
    """
    Replace all numbers in the input text with the dollar sign ($).

    Args:
        text (str): The input text containing numbers.

    Returns:
        str: The text with numbers replaced by dollar signs.
    """
    # Use re.sub to replace all digits (\d+) with $
    result = re.sub(r'\d+', '$', text)
    return result





email_sender = EmailSending(EMAIL_CREDENTIALS_FILE, EMAIL_CREDS_FILE, FROM_EMAIL)