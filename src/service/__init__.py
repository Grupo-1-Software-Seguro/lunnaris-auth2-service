from model.dto import *
from model.dao import *
from model import *
import bcrypt
from flask_jwt_extended import create_access_token
import exceptions

class AuthService:

    dao: AuthDAO

    def __init__(self) -> None:
        self.dao = AuthDAO()

    def register(self, body: AuthModel):
        auth = UserAuth()
        auth.userId = body.userId
        auth.email = body.email
        auth.password = self.hash_password(body.password)
        if self.dao.get_by_email(auth.email):
            raise exceptions.AlreadyRegistered(auth.email)

        self.dao.register(auth)
        return True

    def hash_password(self, password: str) -> str:
        password_bytes = password.encode("utf-8")
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_bytes.decode('utf-8')

    def check_password(self, plain_password: str, hashed_password: str):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def login(self, creds: LoginModel) -> str:
        auth_registry = self.dao.get_by_email(creds.email)
        
        if not auth_registry:
            raise exceptions.InvalidCredentials
        
        if not self.check_password(creds.password, auth_registry.password):
            raise exceptions.InvalidCredentials
        
        return create_access_token(auth_registry.userId)
