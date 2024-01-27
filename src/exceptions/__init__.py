from werkzeug.exceptions import HTTPException
from werkzeug.sansio.response import Response


class InvalidCredentials(HTTPException):
    code = 400
    description = "Credenciales inválidas"


class NotAuthenticated(HTTPException):
    code = 401
    description = "Este recurso requiere autenticación"


class NotAuthorized(HTTPException):
    code = 403
    description = "No estás autorizado para acceder a esta función o recurso"


class InvalidToken(HTTPException):
    code = 400
    description = "No se pudo validar el token"


class AlreadyRegistered(HTTPException):
    
    def __init__(self, email, description: str | None = None, response: Response | None = None) -> None:
        super().__init__(description, response)
        self.code = 400
        self.description = f"Ya existe un registro para {email}"