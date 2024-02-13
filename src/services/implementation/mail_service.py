import os
from flask import render_template
from services.interface.mail_service_interface import IMailService
from flask_mail import Mail, Message


class FlaskMailService(IMailService):

    def __init__(self, mail: Mail) -> None:
        super().__init__()
        self.mail = mail
    
    def send_reset_password_email(self, username: str, email: str, token: str):
        reset_link = os.getenv("RECOVER_URL") + token
    
        msg_body = render_template("mail2.html", username=username, reset_link=reset_link)
        
        msg = Message(
            subject="Cambio de contraseña - Lunnaris",
            sender=os.getenv("EMAIL_SENDER"),
            recipients=[email]
        )
        msg.html = msg_body

        self.mail.send(msg)

from tasks.config_tasks import celery_app
class QueuedMailService(IMailService):

    def send_reset_password_email(self, username: str, email: str, token: str):
        reset_link = os.getenv("RECOVER_URL") + token
        args = {
            "reset_link": reset_link,
            "email": email,
            "username": username
        }

        celery_app.send_task(
            "notifications.send_password_recover_email",
            kwargs=args)
        
