from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from functools import wraps
from services.implementation.auth_service import AuthService
from services.auth_service_interface import IAuthService
from services.implementation.mail_service import FlaskMailService
from services.implementation.token_service import TokenGenerator
from dao.implementation.dao_mongodb import MongoAuthDAO
import inspect

class ProviderMeta(type):

    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]



class ServiceProvider(metaclass=ProviderMeta):

    def __init__(self) -> None:
        self.mail = None
        self.cors = None
        self.jwt = None
        self.service = None

    def init_app(self, app):
        self.mail = Mail(app)
        self.cors = CORS(app, origins="*")
        #self.jwt = JWTManager(app)

    def get_service(self):
        if not self.service:
            self.service = AuthService(
                dao=MongoAuthDAO(),
                mail=FlaskMailService(self.mail),
                token_generator=TokenGenerator()
            )

        return self.service


def use_service(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        parameters = inspect.signature(f).parameters
        for param in parameters.values():
            if param.annotation == IAuthService:
                kwargs[param.name] = ServiceProvider().get_service()
                break
            
        return f(*args, **kwargs)
    return decorated_function


