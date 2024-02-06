from functools import wraps
from .responses import ApiResponse

def api_response(type="object"):
    def super_function(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)
            if isinstance(response, tuple) and len(response) == 2:
                body, status = response
                return ApiResponse(type=type, body=body).model_dump(), status
            
            return ApiResponse(type=type, body=response).model_dump()
        return decorated_function
    return super_function