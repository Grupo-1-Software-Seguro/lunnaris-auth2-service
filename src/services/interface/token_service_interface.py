from abc import ABC, abstractmethod
from entities.auth_registry import AuthRegistry


class ITokenGenerator(ABC):

    @abstractmethod
    def create_login_token(self, credentials: AuthRegistry, minute_expiration: int) -> str:
        pass

    @abstractmethod
    def create_recovery_token(self, user_id: str, minute_expiration: int) -> str:
        pass

    @abstractmethod
    def read_token(self, token: str) -> dict:
        pass
    
    @abstractmethod
    def create_refresh_token(self, user_id: str, days: int = 10) -> str:
        pass
