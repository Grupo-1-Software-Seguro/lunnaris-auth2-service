from flask import Blueprint
from services import IAuthService
from dto.requests import *
from dto.responses import ApiResponse
from lunnaris_pyinject import inject
from provider import Provider, M
AuthRoutes = Blueprint("auth", __name__)


@AuthRoutes.post("/register")
@inject
def register(
    body: RegisterUserRequest = M(RegisterUserRequest), 
    service: IAuthService = Provider.service):

    response = service.register_user(body)
    return ApiResponse(type="object", body=response).model_dump()


@AuthRoutes.post("/login")
@inject
def login(
    body: LoginRequest = M(LoginRequest), 
    service: IAuthService = Provider.service):

    response = service.login(body)
    return ApiResponse(type="object", body=response).model_dump()


@AuthRoutes.post("/reset_password")
@inject
def request_reset_password(
    body: ResetPasswordRequest = M(ResetPasswordRequest), 
    service: IAuthService = Provider.service):

    response = service.request_password_reset(body)
    return ApiResponse(type="object", body=response).model_dump()


@AuthRoutes.put("/reset_password")
@inject
def reset_password(
    body: NewPasswordRequest = M(NewPasswordRequest), 
    service: IAuthService = Provider.service):

    response = service.set_new_password(body)
    return ApiResponse(type="object", body=response).model_dump()



@AuthRoutes.post("/authorize")
@inject
def authorize(
    body: AuthorizeRequest = M(AuthorizeRequest), 
    service: IAuthService = Provider.service):

    response = service.authorize(body)
    return ApiResponse(type="object", body=response).model_dump()


@AuthRoutes.post("/authenticate")
@inject
def authenticate(
    body: AuthenticateRequest = M(AuthenticateRequest), 
    service: IAuthService = Provider.service):

    response = service.authenticate(body)
    return ApiResponse(type="object", body=response).model_dump()


@AuthRoutes.post("/refresh_token")
@inject
def refresh_token(
        body: RefreshTokenRequest = M(RefreshTokenRequest),
        service: IAuthService = Provider.service
    ):

    response = service.refresh_token(body)
    return ApiResponse(type="object", body=response).model_dump(), 201
