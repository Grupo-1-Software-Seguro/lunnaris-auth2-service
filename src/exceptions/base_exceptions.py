class ServiceException(Exception):
    code: int
    description: str
    error_code: str    


def exception_to_json(ex):
    from pydantic import ValidationError
    from werkzeug.exceptions import HTTPException
    code = 500
    response = {
        "type": "error",
        "body": {}
    }

    if isinstance(ex, ServiceException):
        response["body"] = {
            "message": ex.description,
            "status": ex.code,
            "error_code": ex.error_code
        }
        code = ex.code

    elif isinstance(ex, HTTPException):
        response["body"] = {
            "message": ex.description,
            "status": ex.code,
            "error_code": "http"
        }
        code = ex.code

    elif isinstance(ex, ValidationError):

        code = 400
        response["body"] = {
            "message": str(ex.errors()[0]['msg']),
            "status": 400,
            "error_code": "validation"
        }

    else:

        with open("log.txt", "a") as f:
            f.write("\n===\n")
            f.write(f"{type(ex)}: {str(ex)}")

        response["body"] = {
            "message": "Error en el servidor",
            "status": code,
            "error_code": "server_error"
        }

    return response, code

