import datetime
from services.token_service_interface import ITokenGenerator
from utils.jwt import create_token, read_token

class TokenGenerator(ITokenGenerator):

    def create_token(self, user_id: str, minute_expiration: int = 10) -> str:
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