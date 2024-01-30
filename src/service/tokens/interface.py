from abc import ABC, abstractclassmethod

class TokenService(ABC):
    @classmethod
    def create_access_token(self, user) -> str:
        pass
    