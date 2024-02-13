from flask import Blueprint, request
from services import IAuthService
from dto.requests import *
from dto.decorators import api_response
from utils.validation import validate_with_models
from utils.tokens.decorators import jwt_token
from lunnaris_pyinject import inject
from config import Configuration
AuthRoutes = Blueprint("auth", __name__)


@AuthRoutes.post("/register")
@api_response()
@validate_with_models()
@inject
def register(body: RegisterUserRequest, service: IAuthService = Configuration.service):
    return service.register_user(body)


@AuthRoutes.post("/login")
@api_response()
@validate_with_models()
@inject
def login(body: LoginRequest, service: IAuthService = Configuration.service):
    return service.login(body), 201


@AuthRoutes.post("/reset_password")
@api_response()
@validate_with_models()
@inject
@jwt_token
def request_reset_password(body: ResetPasswordRequest, service: IAuthService = Configuration.service):
    return service.request_password_reset(body)


@AuthRoutes.put("/reset_password")
@api_response()
@validate_with_models()
@inject
@jwt_token
def reset_password(body: NewPasswordRequest, service: IAuthService = Configuration.service):
    return service.set_new_password(body)


@AuthRoutes.post("/authorize")
@api_response()
@validate_with_models()
@inject
def authorize(body: AuthorizeRequest, service: IAuthService = Configuration.service):
    return service.authorize(body)


@AuthRoutes.post("/authenticate")
@api_response()
@validate_with_models()
@inject
def authenticate(body: AuthenticateRequest, service: IAuthService = Configuration.service):
    return service.authenticate(body)
