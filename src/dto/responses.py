from typing import Any
from pydantic import BaseModel


class LoginTokenResponse(BaseModel):
    token: str
    id: str


class ResetPasswordResponse(BaseModel):
    token: str


class NewPasswordResponse(BaseModel):
    password_changed: bool


class RegisterUserResponse(BaseModel):
    state: bool


class ApiResponse(BaseModel):
    type: str
    body: Any


class AuthorizeResponse(BaseModel):
    authorized: bool


class AuthenticateResponse(BaseModel):
    authenticated: bool