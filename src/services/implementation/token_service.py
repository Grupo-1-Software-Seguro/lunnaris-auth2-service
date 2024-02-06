import datetime
from services.token_service_interface import ITokenGenerator
from utils.jwt import create_token, read_token


class TokenGenerator(ITokenGenerator):

    def create_login_token(self, user_id: str, minute_expiration: int) -> str:
        today = datetime.datetime.now()
        delta = datetime.timedelta(minutes=minute_expiration)
        exp = today + delta
        payload = {
            "id": user_id,
            "exp": exp.timestamp()
        }

        return create_token(payload)

    def create_recovery_token(self, user_id: str, minute_expiration: int) -> str:
        today = datetime.datetime.now()
        delta = datetime.timedelta(minutes=minute_expiration)
        exp = today + delta
        payload = {
            "id": user_id,
            "exp": exp.timestamp()
        }

        return create_token(payload)

    def read_token(self, token: str) -> dict:
        return read_token(token)


from flask_jwt_extended import create_access_token


class FlaskTokenGenerator(ITokenGenerator):

    def create_login_token(self, user_id: str, minute_expiration: int) -> str:
        return create_access_token(user_id)

    def create_recovery_token(self, user_id: str, minute_expiration: int) -> str:
        today = datetime.datetime.now()
        delta = datetime.timedelta(minutes=minute_expiration)
        exp = today + delta
        payload = {
            "id": user_id,
            "exp": exp.timestamp()
        }
        return create_token(payload)

    def read_token(self, token: str) -> dict:
        return read_token(token)
