import base64
import logging
import os.path
import pickle
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors
from googleapiclient.discovery import build


def send_email(sender, recipient, subject, body) -> None:
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      body: The text of the email message.
    """
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)
    # Service
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send",
    ]
    credentials = None
    if os.path.exists("token.pickle"):
        credentials = pickle.load(open("token.pickle", "rb"))  # Refresh tokens
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        pickle.dump(credentials, open("token.pickle", "wb"))  # Save credentials
    service = build("gmail", "v1", credentials=credentials)
    # Email
    message = MIMEText(body)
    message["from"] = sender
    message["to"] = recipient
    message["subject"] = subject
    try:
        sent_message = (
            service.users()
            .messages()
            .send(
                userId=sender,
                body={
                    "raw": base64.urlsafe_b64encode(
                        message.as_string().encode("utf-8")
                    ).decode("utf-8")
                },
            )
            .execute()
        )
        logging.info("Message id: %s", sent_message["id"])
    except errors.HttpError as error:
        logging.error("An HTTP error occurred: %s", error)
