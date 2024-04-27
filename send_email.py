import smtplib
import ssl
import os.path
from dotenv import load_dotenv

import google.auth.exceptions
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
import base64
from email.mime.text import MIMEText

load_dotenv()
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly"
]

default_receiver = os.getenv('RECEIVER')

message_body = """\
Direct execution of send_email.py succeeded!"""

message_subject = "From Portfolio Website with Love(Debug Backend Mode)"


def authenticator():
    '''Authenticates gmail account and saves as session token.json,
    instead of ephemeral session where user needs to authenticate on
    each API call.
    Also handles invalid and/or expired credentials and token.
    '''
    creds = None
    if os.path.exists("token.json") and os.path.getsize('token.json') != 0:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if os.path.exists('credentials.json'):
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
    else:
        instruction = ('https://mailtrap.io/blog/python-send-email-gmail'
                       '/#How-to-send-an-email-with-Python-via-Gmail-API')
        print(f'Please visit {instruction} to learn how to obtain secret '
              f'file and place it under the same directory '
              f'as send_email.py file.')

    return creds


def send_email(message_body, message_subject_param=message_subject,
               receiver=default_receiver):
    print('line 54-', message_subject_param)
    creds = authenticator()
    try:
        service = build('gmail', 'v1', credentials=creds)
    except google.auth.exceptions.DefaultCredentialsError as e:
        print(e)
        instruction = ('https://mailtrap.io/blog/python-send-email-gmail'
                       '/#How-to-send-an-email-with-Python-via-Gmail-API')
        print(f'Alternatively, please visit {instruction} on how to'
              f' obtain secret file and place it under the same directory '
              f'as send_email.py file.')

    message = MIMEText(message_body)
    message['to'] = receiver
    message['subject'] = message_subject_param
    create_message = {
        'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    try:
        message = (service.users().messages().send(userId="me",
                                                   body=create_message).execute())
        print(message)
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None
    except:
        print('Sum Ting Wong')
        message = None

    return message


if __name__ == "__main__":
    send_email(message_body, message_subject)
