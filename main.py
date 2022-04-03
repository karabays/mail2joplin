from joplin import JoplinNote
import read_emails

emails = read_emails.read_emails()

for email in emails:
    note = JoplinNote()

    note.title = email.subject

    if email.content_html:
        note.body_html = email.content_html
    else:
        note.body = email.content_text

    note_id = note.post_note()

    read_emails.delete_email(email.message_id)
    print(note_id)

read_emails.expunge()

    
