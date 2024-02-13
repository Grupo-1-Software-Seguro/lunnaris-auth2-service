from pydantic import BaseModel


class LoginRequest(BaseModel):
    """
    Login request using the email and the password
    """
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
    userType: int


class AuthorizeRequest(BaseModel):
    token: str
    action: str


class AuthenticateRequest(BaseModel):
    token: str