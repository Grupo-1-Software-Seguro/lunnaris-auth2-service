from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from service import *
from functools import wraps


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



class Provider(metaclass=ProviderMeta):

    def __init__(self) -> None:
        self.mail = None
        self.cors = None
        self.jwt = None
        self.service = None

    def init_app(self, app):
        self.mail = Mail(app)
        self.cors = CORS(app, origins="*")
        self.jwt = JWTManager(app)

    def get_service(self):
        if not self.service:
            self.service = AuthService(
                AuthDAO(),
                MailService(self.mail),
                UserAPI()
            )

        return self.service


def use_service(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        kwargs["service"] = Provider().get_service()
        return f(*args, **kwargs)
    return decorated_function


