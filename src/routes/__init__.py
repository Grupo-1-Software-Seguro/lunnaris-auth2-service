from flask import Blueprint
from flask_pydantic import validate
from model.dto import *
from service import *


AuthRoutes = Blueprint("auth", __name__)

service = AuthService()


@AuthRoutes.post("/register")
@validate()
def register(body: AuthModel):
    res = service.register(body)
    response = {
        "registered": res
    }
    return ApiResponse(type="object", body=response)

@AuthRoutes.post("/login")
@validate()
def login(body: LoginModel):
    token = service.login(body)
    return ApiResponse(type="object", body={
        "token": token
    })