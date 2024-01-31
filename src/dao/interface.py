from abc import ABC, abstractmethod
from entities.auth_registry import AuthRegistry

class IAuthDAO(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> AuthRegistry:
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> AuthRegistry:
        pass

    @abstractmethod
    def save(self, auth_registry: AuthRegistry) -> bool:
        pass

    @abstractmethod
    def update(self, auth_registry: AuthRegistry) -> bool:
        pass