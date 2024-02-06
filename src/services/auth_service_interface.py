from abc import ABC, abstractmethod
from dto.responses import *
from dto.requests import *


class IAuthService(ABC):

    @abstractmethod
    def login(self, login_request: LoginRequest) -> LoginTokenResponse:
        pass

    @abstractmethod
    def request_password_reset(self, password_reset_request: ResetPasswordRequest) -> ResetPasswordResponse:
        pass

    @abstractmethod
    def set_new_password(self, new_password_request: NewPasswordRequest) -> NewPasswordResponse:
        pass

    @abstractmethod
    def register_user(self, register_user_request: RegisterUserRequest) -> RegisterUserResponse:
        pass
