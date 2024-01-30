from flask import Blueprint, request
from flask_pydantic import validate
from flask_jwt_extended import jwt_required
from utils import extract_token
from model.dto import *
from service2 import *
from provider import Provider


AuthRoutes = Blueprint("auth", __name__)

def service():
    return Provider().get_service()

@AuthRoutes.post("/register")
@validate()
def register(body: AuthModel):
    res = service().register(body)
    response = {
        "registered": res
    }
    return ApiResponse(type="object", body=response)

@AuthRoutes.post("/login")
@validate(body=LoginModel)
def login(body: LoginModel, other: str=""):
    return ApiResponse(type="object", body=service().login(body))


@AuthRoutes.post("/reset_password")
@validate()
def request_reset_password(body: EmailRequest):
    service().user_api.token = extract_token(request)
    response = service().request_reset_password(body)
    return ApiResponse(type="object", body=response)


@AuthRoutes.put("/reset_password")
@validate()
def reset_password(body: PasswordChangeRequest):
    service().user_api.token = extract_token(request)
    response = service().reset_password(body)
    return ApiResponse(type="object", body=response)