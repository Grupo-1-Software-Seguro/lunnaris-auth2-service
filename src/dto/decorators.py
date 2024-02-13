from functools import wraps
from .responses import ApiResponse


def api_response(_type: str = "object"):
    """Wraps a response in a standard object response representation
    Parameters:
        _type: str the type of response from
    """
    def super_function(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)
            if isinstance(response, tuple) and len(response) == 2:
                body, status = response
                return ApiResponse(type=_type, body=body).model_dump(), status

            return ApiResponse(type=_type, body=response).model_dump()

        return decorated_function

    return super_function
