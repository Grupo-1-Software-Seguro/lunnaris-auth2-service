from pydantic import BaseModel
from enum import Enum


class UserType(Enum):
    ADMIN = 1
    USER = 2
    MEDIA_MANAGER = 3


class AuthRegistry(BaseModel):
    userId: str
    email: str
    password: str
    userType: int


class Role(BaseModel):
    type: int
    permissions: list[str]