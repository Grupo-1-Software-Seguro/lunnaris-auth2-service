from werkzeug.exceptions import HTTPException
from model.dto import ApiResponse


def exception_to_json(ex):
    code = 500
    response = ApiResponse(type="error", body={})
    if isinstance(ex, HTTPException):
        response.body = {
            "message": ex.description
        }
        code = ex.code
    else:
        print(ex)
        response.body = "Error en servidor"
    return response.model_dump(), code