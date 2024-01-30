from flask import render_template
from flask_mail import Mail, Message
import os

from .interface import MailService

class FlaskMailService(MailService):

    def __init__(self, mail: Mail) -> None:
        self.mail = mail
        
    def send_password_recover_mail(self, username: str, email: str, token):
        
        reset_link = os.getenv("RECOVER_URL") + token
    
        msg_body = render_template("mail_body.html", username=username, reset_link=reset_link)
        
        msg = Message(
            subject="Cambio de contraseña - Lunnaris",
            sender=os.getenv("EMAIL_SENDER"),
            recipients=[email]
        )
        msg.html = msg_body
        print("previo de enviar el email")
        self.mail.send(msg)
        