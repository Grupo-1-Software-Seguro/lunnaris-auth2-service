from pydantic import BaseModel, Field, field_validator

characters = "#?@$%&!¡¿="

class ApiResponse(BaseModel):
    type: str
    body: dict


class EmailRequest(BaseModel):
    email: str


class Password(BaseModel):
    password: str

    @field_validator("password")
    def validate_password(cls, val):
        value = str(val)

        if len(value) < 8:
            raise ValueError("La contraseña debe tener 8 caracteres")
        if not any(c.isupper() for c in value):
            raise ValueError("La contraseña debe tener al menos una mayúscula")
        if not any(c.islower() for c in value):
            raise ValueError("La contraseña debe tener al menos una minúscula")
        if not any(c.isdigit() for c in value):
            raise ValueError("La contraseña debe tener al menos un dígito")
        if not any(c in characters for c in value):
            raise ValueError(f"La contraseña debe tener al menos un caracter especial {characters}")

        return value


class PasswordChangeRequest(Password):
    token: str


class AuthModel(Password):
    userId: str
    email: str


class LoginModel(Password):
    email: str