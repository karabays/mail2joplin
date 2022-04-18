
from base64 import decode
from dataclasses import dataclass, field
from enum import Enum
from imaplib import IMAP4_SSL
import email
from email import policy
import string
from loguru import logger
from imbox import Imbox

from config import emailConf

imap = IMAP4_SSL(emailConf.server,port=emailConf.port)
imap.login(emailConf.user, emailConf.passw)
imap.select("INBOX")

class NoteType(Enum):
    NOTE = 'note'
    TASK = 'task'

@dataclass
class Email:
    message_id: int
    subject: string = ''
    content_text: string = ''
    content_html: string = ''
    attachments: list[bytes] = field(default_factory=list)
    type: NoteType = NoteType.NOTE


def check_email():
    status, data = imap.search(None,'ALL')
    mail_ids = []
    for block in data:
        mail_ids += block.split()
    if len(mail_ids):
        logger.info(f"Found {len(mail_ids)} mail(s).")
    else:
        logger.info('No mails found')
    return mail_ids
    
def read_emails():
    email_ids = check_email()
    emails = []
    for i in email_ids:
        status, data = imap.fetch(i,'(RFC822)')
        msg = email.message_from_bytes(data[0][1],policy=policy.default)
        email_message = {}
        attachments = []
        for part in msg.walk():
            if part.get_filename():
                attachments.append({part.get_filename(): part.get_payload()})
            if part.get_content_type == "text/plain":
                email_message['content_text'] = part.get_payload()
            if part.get_content_type() == 'text/html':
                email_message['content_html'] = part.get_payload()
            email_message['attachments'] = attachments
        email_message['subject'] = msg['subject']
        email_message['message_id'] = i
        
        mail = Email(**email_message)
        emails.append(mail)
        logger.info(f"email with subject: {email_message['subject']} is read.")
        logger.debug(mail)
    return emails

def delete_email(msg_id):
    imap.store(msg_id,'+FLAGS', '\\Deleted')
    logger.info(f"{msg_id} is marked for deletion.")


def expunge():
    imap.expunge()
    logger.info('inbox expunged...')


if __name__ == "__main__":
    
    read_emails()
    
