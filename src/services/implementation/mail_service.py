import os
from flask import render_template
from services.mail_service_interface import IMailService
from flask_mail import Mail, Message

class FlaskMailService(IMailService):

    def __init__(self, mail: Mail) -> None:
        super().__init__()
        self.mail = mail
    
    def send_reset_password_email(self, username: str, email: str, token: str):
        reset_link = os.getenv("RECOVER_URL") + token
    
        msg_body = render_template("mail_body.html", username=username, reset_link=reset_link)
        
        msg = Message(
            subject="Cambio de contraseña - Lunnaris",
            sender=os.getenv("EMAIL_SENDER"),
            recipients=[email]
        )
        msg.html = msg_body
        self.mail.send(msg)