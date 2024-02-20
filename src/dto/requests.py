from pydantic import BaseModel, field_validator

class PasswordValidator(BaseModel):

    password: str

    @field_validator("password")
    def password_validation(cls, value: str) -> str:
        special_chars = "@%$!¡¿?#&"

        if len(value) < 12 or len(value) > 50:
            raise ValueError("La contraseña debe tener de 12 a 50 caracteres")
        
        if not any([c.isupper() for c in value]):
            raise ValueError("La contraseña debe tener al menos una letra mayúscula")
    
        if not any([c.islower() for c in value]):
            raise ValueError("La contraseña debe tener al menos una letra minúscula")
    
        if not any([c.isnumeric() for c in value]): 
            raise ValueError("La contraseña debe tener al menos un número")
        
        if not any([c in special_chars for c in value]): 
            raise ValueError(f"La contraseña debe tener al menos un caracter especial: {special_chars}")

        return value


class LoginRequest(BaseModel):
    """
    Login request using the email and the password
    """
    email: str
    password: str


class ResetPasswordRequest(BaseModel):
    email: str


class NewPasswordRequest(PasswordValidator):
    token: str


class RegisterUserRequest(PasswordValidator):
    userId: str
    email: str
    userType: int

    @field_validator("userType", mode="after")
    def user_type_validation(cls, value: int):
        from entities.auth_registry import UserType

        user_types = [u.value for u in UserType]
        if value not in user_types:
            raise ValueError(f"Tipo de usuario desconocido: {value}")
        return value

class AuthorizeRequest(BaseModel):
    token: str
    action: str


class AuthenticateRequest(BaseModel):
    token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
