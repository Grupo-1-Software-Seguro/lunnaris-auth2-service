from werkzeug.exceptions import HTTPException
from dto.responses import ApiResponse
import datetime
import os
import jwt

HASH = "HS256"

def exception_to_json(ex: Exception):
    from pydantic import ValidationError
    code = 500
    response = ApiResponse(type="error", body={})
    if isinstance(ex, HTTPException):
        response.body = {
            "message": ex.description,
            "status": ex.code
        }
        code = ex.code
    elif isinstance(ex, ValidationError):
        code = 400
        response.body = {
            "message": str(ex.errors()[0]['msg']),
            "status": 400
        }

    else:

        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"{type(ex)}: {str(ex)}")
        
        response.body = {
            "message": "Error interno",
            "status": 500
        }

    return response.model_dump(), code


def exception_on_value(value, comparison, exception):
    if value == comparison:
        raise exception
    return value



def create_recover_token(userId: str, minutes=10):
    today = datetime.datetime.now()
    delta = datetime.timedelta(minutes=minutes)
    exp = today + delta
    return jwt.encode({"id": userId, "exp": exp.timestamp()}, os.getenv("RECOVERY_SECRET"), HASH)


def validate_recover_token(token):
    try:
        return jwt.decode(token, os.getenv("RECOVERY_SECRET"), HASH)
    except jwt.DecodeError:
        return None


def extract_token(request):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        return auth_header.removeprefix("Bearer").strip()
    return None