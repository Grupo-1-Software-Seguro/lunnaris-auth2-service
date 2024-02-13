from abc import ABC, abstractmethod


class IMailService:
    @abstractmethod
    def send_reset_password_email(self, username: str, email: str, token: str):
        pass
