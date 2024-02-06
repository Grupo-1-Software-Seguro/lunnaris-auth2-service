from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class ResetPasswordRequest(BaseModel):
    email: str


class NewPasswordRequest(BaseModel):
    token: str
    password: str


class RegisterUserRequest(BaseModel):
    userId: str
    email: str
    password: str
    fullName: str