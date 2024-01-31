from flask import Blueprint, request
from provider import use_service
from services.auth_service_interface import IAuthService
from dto.requests import *
from dto.responses import *
from utils.validation import validate_with_models

AuthRoutes = Blueprint("auth", __name__)


@AuthRoutes.post("/register")
@validate_with_models()
@use_service
def register(body: RegisterUserRequest, service: IAuthService):
    res = service.register_user(body)
    return res.model_dump()

@AuthRoutes.post("/login")
@validate_with_models()
@use_service
def login(body: LoginRequest, service: IAuthService):
    return service.login(body).model_dump()


@AuthRoutes.post("/reset_password")
@validate_with_models()
@use_service
def request_reset_password(body: ResetPasswordRequest, service: IAuthService):
    response = service.request_password_reset(body)
    return response.model_dump()


@AuthRoutes.put("/reset_password")
@validate_with_models()
@use_service
def reset_password(body: NewPasswordRequest, service: IAuthService):
    response = service.set_new_password(body)
    return response.model_dump()