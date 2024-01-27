from pydantic import BaseModel


class AuthModel(BaseModel):
    userId: str
    email: str
    password: str


class LoginModel(BaseModel):
    email: str
    password: str

class ApiResponse(BaseModel):
    type: str
    body: dict
