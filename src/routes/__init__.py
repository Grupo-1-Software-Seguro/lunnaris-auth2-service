from flask import Blueprint
from services import IAuthService
from dto.requests import *
from dto.responses import ApiResponse
from lunnaris_pyinject import inject
from config import Configuration, model
AuthRoutes = Blueprint("auth", __name__)


@AuthRoutes.post("/register")
@inject
def register(
    body: RegisterUserRequest = model(RegisterUserRequest), 
    service: IAuthService = Configuration.service):

    response = service.register_user(body)
    return ApiResponse(type="object", body=response).model_dump()


@AuthRoutes.post("/login")
@inject
def login(
    body: LoginRequest = model(LoginRequest), 
    service: IAuthService = Configuration.service):

    response = service.login(body)
    return ApiResponse(type="object", body=response).model_dump()


@AuthRoutes.post("/reset_password")
@inject
def request_reset_password(
    body: ResetPasswordRequest = model(ResetPasswordRequest), 
    service: IAuthService = Configuration.service):

    response = service.request_password_reset(body)
    return ApiResponse(type="object", body=response).model_dump()


@AuthRoutes.put("/reset_password")
@inject
def reset_password(
    body: NewPasswordRequest = model(NewPasswordRequest), 
    service: IAuthService = Configuration.service):

    response = service.set_new_password(body)
    return ApiResponse(type="object", body=response).model_dump()



@AuthRoutes.post("/authorize")
@inject
def authorize(
    body: AuthorizeRequest = model(AuthorizeRequest), 
    service: IAuthService = Configuration.service):

    response = service.authorize(body)
    return ApiResponse(type="object", body=response).model_dump()


@AuthRoutes.post("/authenticate")
@inject
def authenticate(
    body: AuthenticateRequest = model(AuthenticateRequest), 
    service: IAuthService = Configuration.service):

    response = service.authenticate(body)
    return ApiResponse(type="object", body=response).model_dump()


@AuthRoutes.post("/refresh_token")
@inject
def refresh_token(
        body: RefreshTokenRequest = model(RefreshTokenRequest),
        service: IAuthService = Configuration.service
    ):

    response = service.refresh_token(body)
    return ApiResponse(type="object", body=response).model_dump(), 201
