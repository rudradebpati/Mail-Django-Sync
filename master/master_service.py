# fetch_emails.py
import imaplib2
import email
import os
from dotenv import load_dotenv
from datetime import datetime
import logging
from email import utils, errors
from typing import List,TypedDict

# Configure logging
error_logger = logging.getLogger(__name__)

load_dotenv()
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')

class EmailData(TypedDict):
    subject: str
    sender: str
    body: str
    date_received: datetime

def fetch_emails()->List[EmailData]:
    mail = imaplib2.IMAP4_SSL(EMAIL_HOST)
    try:
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select('INBOX')

        status, data = mail.search(None, 'UNSEEN')
        if status != 'OK':
            error_logger.info("No unseen emails found.")
            return []
        result_list=[]
        for num in data[0].split():
            status, msg_data = mail.fetch(num, '(RFC822)')
            if status != 'OK':
                error_logger.error(f"Failed to fetch email ID {num}")
                continue

            if isinstance(msg_data[0], tuple):
                raw_email = msg_data[0][1]

            msg = email.message_from_bytes(raw_email)
            if not msg:
                error_logger.error(f"Failed to parse email ID {num}")
                continue
            subject = msg.get('subject', '(No Subject)')
            sender = msg.get('from', '')
            date_received = msg.get('date', '')

            # Parse the email body
            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_dispo = str(part.get('Content-Disposition'))

                    if content_type == 'text/plain' and 'attachment' not in content_dispo:
                        try:
                            body += part.get_payload(decode=True).decode(errors='ignore')
                        except Exception as e:
                            error_logger.warning(f"Failed to decode email body part: {e}")
            else:
                body = msg.get_payload(decode=True).decode(errors='ignore')

            # Parse the date properly
            try:
                parsed_date = utils.parsedate_to_datetime(date_received)
            except Exception:
                error_logger.warning(f"Failed to parse date: {date_received}. Using current timestamp.")
                parsed_date = datetime.now()

            result_list.append({
                'subject': subject,
                'sender': sender,
                'body': body,
                'date_received': parsed_date
            })
        return result_list
    except imaplib2.IMAP4.error as e:
        error_logger.error(f"IMAP error: {e}")
        return []
    except errors.MessageError as e:
        error_logger.error(f"Email parsing error: {e}")
        return []
    except Exception as e:
        error_logger.error(f"Unexpected error: {e}")
        return []
    finally:
        try:
            mail.logout()
        except Exception as e:
            error_logger.warning(f"Failed to logout from IMAP server: {e}")
