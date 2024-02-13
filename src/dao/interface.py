from abc import ABC, abstractmethod
from entities.auth_registry import AuthRegistry, Role


class IAuthDAO(ABC):
    """
    Interface for DAO object
    """
    @abstractmethod
    def get_by_email(self, email: str) -> AuthRegistry:
        """
        Parameters:
            email: str the user email
        Returns:
            the **AuthRegistry** associated with the passed email
        """

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> AuthRegistry:
        """
        Parameters:
            user_id: str the user unique identifier
        Returns:
            the **AuthRegistry** associated with the passed email
        """

    @abstractmethod
    def save(self, auth_registry: AuthRegistry) -> bool:
        """
        Parameters:
            auth_registry: AuthRegistry
        Returns:
            bool representing the state of the operation, whether it's saved or not.
        """

    @abstractmethod
    def update(self, auth_registry: AuthRegistry) -> bool:
        """
        Parameters:
            auth_registry: AuthRegistry
        Returns:
            bool representing the state of the operation, whether it's updated or not.
        """
        pass
    
    @abstractmethod
    def get_role(self, type: int) -> Role:
        pass
