from model import *
class AuthDAO:

    def register(self, auth: UserAuth) -> UserAuth:
        auth.save()
        return auth

    def get_by_email(self, email: str) -> UserAuth:
        return UserAuth.objects(email=email).first()