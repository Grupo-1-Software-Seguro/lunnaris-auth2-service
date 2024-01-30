from model import *
from abc import ABC, ABCMeta, abstractmethod

from model import UserAuth

class AuthDAO(ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> UserAuth:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> UserAuth:
        pass

    @abstractmethod
    def save(self, auth: UserAuth) -> UserAuth:
        pass


class MongoAuthDAO(AuthDAO):

    def get_by_email(self, email: str) -> UserAuth:
        return UserAuth.objects(email=email).first()

    def get_by_id(self, id: str) -> UserAuth:
        return UserAuth.objects(userId=id).first()
    
    def save(self, auth: UserAuth) -> UserAuth:
        auth.save()
        return auth