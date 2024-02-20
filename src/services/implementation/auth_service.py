from dto.requests import RefreshTokenRequest
from dto.responses import RefreshTokenResponse
from services.interface.auth_service_interface import IAuthService
from dto.requests import AuthenticateRequest, AuthorizeRequest, LoginRequest, NewPasswordRequest, RegisterUserRequest, ResetPasswordRequest
from dto.responses import AuthenticateResponse, AuthorizeResponse, LoginTokenResponse, NewPasswordResponse, RegisterUserResponse, ResetPasswordResponse
from dao.interface import IAuthDAO
from entities.auth_registry import AuthRegistry, UserType
from services.interface.token_service_interface import ITokenGenerator
from services.interface.mail_service_interface import IMailService
from exceptions import *
from utils.password import check_password, hash_password
from lunnaris_pyinject import inject


class AuthService(IAuthService):
    @inject
    def __init__(self, dao: IAuthDAO, token_generator: ITokenGenerator, mail: IMailService) -> None:
        super().__init__()
        self.dao = dao
        self.token_handler = token_generator
        self.mail = mail

    def login(self, login_request: LoginRequest) -> LoginTokenResponse:
        auth_registry = self.dao.get_by_email(login_request.email)
        if not auth_registry:
            raise InvalidCredentials

        if not check_password(login_request.password, auth_registry.password):
            raise InvalidCredentials

        return LoginTokenResponse(
            token=self.token_handler.create_login_token(auth_registry),
            id=auth_registry.userId,
            refresh=self.token_handler.create_refresh_token(auth_registry.userId)
        )
    

    def register_user(self, register_user_request: RegisterUserRequest) -> RegisterUserResponse:
        if self.dao.get_by_email(register_user_request.email):
            raise AlreadyRegistered(register_user_request.email)

        if register_user_request.userType not in [member.value for member in UserType]:
            raise UnknownRole(register_user_request.userType)

        auth_registry = AuthRegistry(
            userId=register_user_request.userId,
            email=register_user_request.email,
            password=hash_password(register_user_request.password),
            userType=register_user_request.userType
        )

        return RegisterUserResponse(
            state=self.dao.save(auth_registry)
        )

    def request_password_reset(self, password_reset_request: ResetPasswordRequest) -> ResetPasswordResponse:
        auth_registry = self.dao.get_by_email(password_reset_request.email)

        if not auth_registry:
            raise NotRegistered

        recover_token = self.token_handler.create_recovery_token(auth_registry.userId, 10)
        token = self.token_handler.create_login_token(auth_registry, 10)
        self.mail.send_reset_password_email(recover_token, auth_registry.userId, token)
        return ResetPasswordResponse(token=recover_token)

    def set_new_password(self, new_password_request: NewPasswordRequest) -> NewPasswordResponse:
        payload = self.token_handler.read_token(new_password_request.token)
        if not payload:
            raise InvalidToken

        auth_registry = self.dao.get_by_user_id(payload["id"])
        auth_registry.password = hash_password(new_password_request.password)

        return NewPasswordResponse(
            password_changed=self.dao.update(auth_registry)
        )

    def authorize(self, authorize_request: AuthorizeRequest) -> AuthorizeResponse:
        token = self.token_handler.read_token(authorize_request.token)
        if not token:
            raise InvalidToken
        
        token_type = token.get("type")

        if not token_type:
            raise InvalidToken

        role = self.dao.get_role(token_type)
        
        if not role:
            return AuthorizeResponse(authorized=False)
        
        if authorize_request.action in role.permissions:
            return AuthorizeResponse(authorized=True)
        
        return AuthorizeResponse(authorized=False)
    
    def authenticate(self, authenticate_request: AuthenticateRequest) -> AuthenticateResponse:
        payload = self.token_handler.read_token(authenticate_request.token)
        if not payload:
            return AuthenticateResponse(authenticated=False)
        else:
            return AuthenticateResponse(authenticated=True)
    
    def refresh_token(self, refresh_token_request: RefreshTokenRequest) -> RefreshTokenResponse:
        payload = self.token_handler.read_token(refresh_token_request.refresh_token)

        if not payload:
            raise InvalidToken
        
        user_id = payload.get("id")
        token_type = payload.get("token_type")

        if not payload or token_type != "refresh_token":
            raise InvalidToken
        
        audit_registry = self.dao.get_by_user_id(user_id)
        
        if not audit_registry:
            raise NotRegistered
        
        token = self.token_handler.create_login_token(audit_registry)

        return RefreshTokenResponse(token=token)
        
