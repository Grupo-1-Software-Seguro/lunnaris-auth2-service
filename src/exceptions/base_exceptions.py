class ServiceException(Exception):
    """
    Base class for service exception, contains the following attributes:
    :param description, human readable string for the error
    :param error_code, machine readable string for the error
    :param code, int number to determine the status for the service failure
    """


    code: int = 500
    description: str = "Service error"
    error_code: str = "service_error"

    def __init__(self, description=None, error_code=None, code=None) -> None:
        super().__init__()
        if description:
            self.description = description

        if error_code:
            self.error_code = error_code

        if code:
            self.code = code    

    def __str__(self) -> str:
        return self.description

def exception_to_json(ex):
    """
    Transforms an exception to json so it can be send as an error to 
    the client. It follows the next structure 
    
    {
        "type": {"type":"string"}, 
        "body": {
            "type":"object", 
            "fields": {
                "message": "string",
                "status": "int",
                "error_code": "string"   
            }
        }   
    }
    
    :param ex, Exception subclass
    """
    from pydantic import ValidationError
    code = 500
    response = {
        "type": "error",
        "body": {
            "message": "Error en el servidor",
            "status": code,
            "error_code": "server_error"
        }
    }

    if hasattr(ex, "code"):
        if ex.code is not None:
            response["body"]["status"] = ex.code
            code = ex.code
    
    if hasattr(ex, "message"):
        if ex.message:
            response["body"]["message"] = ex.message
    
    if hasattr(ex, "description"):
        if ex.description:
            response["body"]["message"] = ex.description
    
    if hasattr(ex, "error_code"):
        if ex.error_code:
            response["body"]["error_code"] = ex.error_code

    if isinstance(ex, ValidationError):

        code = 400
        response["body"] = {
            "message": str(ex.errors()[0]['msg']),
            "status": 400,
            "error_code": "validation"
        }

    return response, code

