import os
from services.interface.mail_service_interface import IMailService

from tasks.config_tasks import celery_app
class QueuedMailService(IMailService):

    def send_reset_password_email(self, recover_token: str, user_id: str, token: str):

        args = {
            "reset_token": recover_token,
            "user_id": user_id,
            "token": token
        }

        celery_app.send_task(
            "notifications.send_password_recover_email",
            kwargs=args)
        
