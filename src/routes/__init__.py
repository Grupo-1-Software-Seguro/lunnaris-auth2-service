from flask import Blueprint, request
from provider import use_service
from services.auth_service_interface import IAuthService
from dto.requests import *
from dto.responses import *
from dto.decorators import api_response
from utils.validation import validate_with_models

AuthRoutes = Blueprint("auth", __name__)


@AuthRoutes.post("/register")
@api_response()
@validate_with_models()
@use_service
def register(body: RegisterUserRequest, service: IAuthService):
    return service.register_user(body)
    #return ApiResponse(type="object", body=res)

@AuthRoutes.post("/login")
@api_response()
@validate_with_models()
@use_service
def login(body: LoginRequest, service: IAuthService):
    return service.login(body), 201
    #return ApiResponse(type="object", body=res)


@AuthRoutes.post("/reset_password")
@api_response()
@validate_with_models()
@use_service
def request_reset_password(body: ResetPasswordRequest, service: IAuthService):
    return service.request_password_reset(body)
    #return ApiResponse(type="object", body=response)


@AuthRoutes.put("/reset_password")
@api_response()
@validate_with_models()
@use_service
def reset_password(body: NewPasswordRequest, service: IAuthService):
    return service.set_new_password(body)
    #return ApiResponse(type="object", body=response)