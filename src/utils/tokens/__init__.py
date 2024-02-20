import jwt
import os

HASH = "HS256"


def create_token(payload: dict) -> str:
    return jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm=HASH)


def read_token(token: str) -> dict:
    try:
        return jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[HASH])
    except jwt.PyJWTError as e:
        print(e)
        return None