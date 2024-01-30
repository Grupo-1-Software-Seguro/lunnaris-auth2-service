from abc import ABC, abstractmethod

class ITokenGenerator(ABC):
    
    @abstractmethod
    def create_token(self, user_id: str, minute_expiration: int) -> str:
        pass

    @abstractmethod
    def read_token(self, token: str) -> dict:
        pass