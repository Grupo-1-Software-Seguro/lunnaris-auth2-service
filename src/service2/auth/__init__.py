from model.dto import *
from model.dao import *
from model import *
from service2.mail.interface import MailService
import bcrypt
from utils import create_recover_token, validate_recover_token, exception_on_value
from exceptions import *
from api import UserAPI
from service2.tokens.interface import TokenService


class AuthService:

    dao: AuthDAO
    mail_service: MailService
    user_api: UserAPI

    def __init__(self, 
                 dao: AuthDAO, 
                 mail_service: MailService, 
                 user_api: UserAPI,
                 tokens: TokenService
                 ) -> None:
        self.dao = dao
        self.mail_service = mail_service
        self.user_api = user_api
        self.tokens = tokens

    def register(self, body: AuthModel):
        if self.dao.get_by_email(body.email):
            raise AlreadyRegistered(body.email)
        
        auth = UserAuth()
        auth.userId = body.userId
        auth.email = body.email
        auth.password = self.hash_password(body.password)
        
        self.dao.save(auth)

        return True

    def hash_password(self, password: str) -> str:
        password_bytes = password.encode("utf-8")
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_bytes.decode('utf-8')

    def check_password(self, plain_password: str, hashed_password: str):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def login(self, creds: LoginModel) -> dict:
        auth_registry = exception_on_value(
            self.dao.get_by_email(creds.email),
            None,
            InvalidCredentials
        )
        
        if not self.check_password(creds.password, auth_registry.password):
            raise InvalidCredentials
        
        return {
            "token": self.tokens.create_access_token(auth_registry.userId),
            "id": auth_registry.userId
            }
    
    def request_reset_password(self, request: EmailRequest):
        #Obtener usuario
        auth = exception_on_value(
            self.dao.get_by_email(request.email),
            None,
            NotRegistered
        )
        
        #Generar token
        token = create_recover_token(auth.userId)
        #Enviar email
        #users = self.user_api.get_users([auth.userId])

        #if len(users) == 0:
        #    raise APIError("Error al cargar datos del usuario")

        username = "Usuario" #users[0].fullName
        self.mail_service.send_password_recover_mail(username, auth.email, token)
        return {
            "token": token
        }
    
    def reset_password(self, request: PasswordChangeRequest):
        payload = exception_on_value(
            validate_recover_token(request.token),
            None,
            InvalidToken
        )
    
        user_id = payload["id"]
        auth = exception_on_value(
            self.dao.get_by_id(user_id),
            None,
            InvalidToken
        )

        new_password = self.hash_password(request.password)
        auth.password = new_password

        self.dao.save(auth)

        return {
            "id": user_id
        }

