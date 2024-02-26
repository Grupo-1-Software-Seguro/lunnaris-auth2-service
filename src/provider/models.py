from lunnaris_pyinject import DependantDependency, Dependency
from pydantic import BaseModel
from typing import Type
from utils.logger import log_to_file


class ModelDependency(Dependency[BaseModel]):
    """
    Dependency that allows to transform the flask request to a pydantic Model.
    """
    def __init__(self, some_type: Type[BaseModel], *args, **kwargs):
        super().__init__(some_type, *args, **kwargs)

    def inject(self) -> BaseModel:
        from flask import request
        return self.some_type(**request.get_json())


class Token(BaseModel):
    id: str
    type: int
    exp: float
    original: str

class TokenDependency(Dependency[Token]):
    def __init__(self):
        pass
    
    def inject(self) -> Token:
        from flask import request
        import base64, json

        token = request.headers.get("Authorization")
        if not token:
            return None
        
        token = token.removeprefix("Bearer ")
        payload = token.split(".")[1]
        payload = base64.b64decode(payload+"==")
        payload = json.loads(payload)
        return Token(**payload, original=token)

def M(some_type):
    """
    Abreviation for creating a ModelDependency object.
    :param some_type, Type that the ModelDependency will use to create 
    the resulting object of injection.
    """
    return ModelDependency(some_type)
