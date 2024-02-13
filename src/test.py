from tasks.email_server import send_email
from dotenv import load_dotenv
import os
load_dotenv(".env")

msg = {
    'sender': 'your_email@example.com',
    'recipients': ['recipient1@example.com', 'recipient2@example.com'],
    'subject': 'Test Email',
    'body': 'This is a test email sent using Python.'
}


send_email(
        msg,
        os.getenv("MAIL_SERVER"),
        int(os.getenv("MAIL_PORT")),
        os.getenv("MAIL_USERNAME"),
        os.getenv("MAIL_PASSWORD")
    )
