from abc import ABC, abstractmethod


class IMailService:
    @abstractmethod
    def send_reset_password_email(self, recover_token: str, user_id: str, token: str):
        pass
