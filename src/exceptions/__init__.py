from .base_exceptions import ServiceException


class InvalidCredentials(ServiceException):
    code = 400
    description = "Credenciales inválidas"
    error_code = "invalid_credentials"


class NotAuthenticated(ServiceException):
    code = 401
    description = "Este recurso requiere autenticación"
    error_code = "authentication"


class NotAuthorized(ServiceException):
    code = 403
    description = "No estás autorizado para acceder a esta función o recurso"
    error_code = "authorization"


class InvalidToken(ServiceException):
    code = 400
    description = "No se pudo validar el token"
    error_code = "token_error"


class AlreadyRegistered(ServiceException):
    code = 400
    error_code = "already_exists"
    description = "Ya existe un registro"

    def __init__(self, email) -> None:
        super().__init__()
        self.code = 400
        self.description = f"Ya existe un registro para {email}"


class NotRegistered(ServiceException):
    code = 404
    description = "El usuario no está registrado"
    error_code = "not_registered"


class APIError(ServiceException):
    code = 400
    error_code = "external"


class NoAuthMethodProvided(ServiceException):
    code = 400
    description = "No se encontró un método de autenticación válido"
    error_code = "authentication_missing"


class UnknownRole(ServiceException):
    code = 400
    error_code = "invalid_role"
    description = "Error en el rol"

    def __init__(self, role) -> None:
        super().__init__()
        self.description = f"Error en el rol: {role}"