from pydantic import BaseModel, field_validator
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

    @field_validator("userType", mode="after")
    def user_type_validation(cls, value: int):
        user_types = [u.value for u in UserType]
        if value not in user_types:
            raise ValueError(f"Tipo de usuario desconocido: {value}")
        return value


class Role(BaseModel):
    type: int
    permissions: list[str]