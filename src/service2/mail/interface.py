from abc import ABC, abstractmethod

class MailService(ABC):
    @abstractmethod
    def send_password_recover_mail(self, username: str, email: str, token):
        pass