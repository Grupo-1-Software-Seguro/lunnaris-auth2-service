import os
from functools import wraps
from flask import request
import jwt
from exceptions import NoAuthMethodProvided, InvalidToken
from . import HASH, Token
import inspect


def jwt_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Authorization" not in request.headers:
            raise NoAuthMethodProvided

        token = request.headers["Authorization"].removeprefix("Bearer ")
        token = Token(token)
        try:
            token.payload = jwt.decode(token.raw, os.getenv("JWT_SECRET_KEY"), algorithms=[HASH])
        except jwt.PyJWTError as e:
            raise InvalidToken

        parameters = [p for p in inspect.signature(f).parameters.values() if p.annotation == Token]
        param = None if len(parameters) == 0 else parameters[0]

        if param:
            kwargs[param.name] = token

        return f(*args, **kwargs)
    return decorated_function
