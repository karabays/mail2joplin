from loguru import logger
from markdownify import markdownify as md

from config import genConf
from joplin import JoplinNote
import read_emails

logger.add('mail2joplin.log')
logger.info('Starting script.')
emails = read_emails.read_emails()

if emails:
    for email in emails:
        note = JoplinNote()
        
        note.title = email.subject
        
        if email.content_html:
            note.body = md(email.content_html)
        else:
            note.body = email.content_text
        note_id = note.post_note()

        read_emails.delete_email(email.message_id)

    read_emails.expunge()

logger.info('script ended.')
    
