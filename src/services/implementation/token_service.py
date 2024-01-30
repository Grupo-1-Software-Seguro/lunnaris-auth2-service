from services.token_service_interface import ITokenGenerator


class TokenGenerator(ITokenGenerator):

    def create_token(self, user_id: str, minute_expiration: int) -> str:
        return super().create_token(user_id, minute_expiration)
    
    def read_token(self, token: str) -> dict:
        return super().read_token(token)