from typing import Type
from lunnaris_pyinject import Dependency
from pydantic import BaseModel
import services
import dao


class ModelDependency(Dependency[BaseModel]):

    def __init__(self, some_type: BaseModel, *args, **kwargs):
        super().__init__(some_type, *args, **kwargs)

    def inject(self) -> BaseModel:
        from flask import request
        self.kwargs.update(request.get_json())
        return super().inject()
    
def model(some_type):
    return ModelDependency(some_type)


class Configuration:
    mail = Dependency(services.QueuedMailService, is_singleton=True)
    token = Dependency(services.TokenGenerator, is_singleton=True)
    dao = Dependency(dao.MongoAuthDAO, is_singleton=True)
    service = Dependency(services.AuthService, dao=dao, token_generator=token, mail=mail, is_singleton=True)
