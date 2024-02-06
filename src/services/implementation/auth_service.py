from services.auth_service_interface import IAuthService
from dto.requests import LoginRequest, NewPasswordRequest, RegisterUserRequest, ResetPasswordRequest
from dto.responses import LoginTokenResponse, NewPasswordResponse, RegisterUserResponse, ResetPasswordResponse
from dao.interface import IAuthDAO
from entities.auth_registry import AuthRegistry
from services.token_service_interface import ITokenGenerator
from services.mail_service_interface import IMailService
from exceptions import *
from utils import exception_on_value
from utils.password import check_password, hash_password


class AuthService(IAuthService):

    def __init__(self, dao: IAuthDAO, token_generator: ITokenGenerator, mail: IMailService) -> None:
        super().__init__()
        self.dao = dao
        self.token_generator = token_generator
        self.mail = mail

    def login(self, login_request: LoginRequest) -> LoginTokenResponse:
        auth_registry = exception_on_value(
            self.dao.get_by_email(login_request.email),
            None,
            InvalidCredentials
        )

        if not check_password(login_request.password, auth_registry.password):
            raise InvalidCredentials

        return LoginTokenResponse(
            token=self.token_generator.create_login_token(auth_registry.userId, 10),
            id=auth_registry.userId
        )

    def register_user(self, register_user_request: RegisterUserRequest) -> RegisterUserResponse:
        if self.dao.get_by_email(register_user_request.email):
            raise AlreadyRegistered(register_user_request.email)

        auth_registry = AuthRegistry(
            userId=register_user_request.userId,
            email=register_user_request.email,
            password=hash_password(register_user_request.password),
            fullName=register_user_request.fullName
        )

        return RegisterUserResponse(
            state=self.dao.save(auth_registry)
        )

    def request_password_reset(self, password_reset_request: ResetPasswordRequest) -> ResetPasswordResponse:
        auth_registry = self.dao.get_by_email(password_reset_request.email)

        if not auth_registry:
            raise NotRegistered

        token = self.token_generator.create_recovery_token(auth_registry.userId, 10)
        self.mail.send_reset_password_email(auth_registry.fullName, password_reset_request.email, token)
        return ResetPasswordResponse(token=token)

    def set_new_password(self, new_password_request: NewPasswordRequest) -> NewPasswordResponse:
        payload = self.token_generator.read_token(new_password_request.token)
        if not payload:
            raise InvalidToken

        auth_registry = self.dao.get_by_user_id(payload["id"])
        auth_registry.password = hash_password(new_password_request.password)

        return NewPasswordResponse(
            password_changed=self.dao.update(auth_registry)
        )
