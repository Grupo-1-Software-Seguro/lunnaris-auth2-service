from lunnaris_pyinject import DependantDependency, Dependency
from pydantic import BaseModel
from typing import Type

class ModelDependency(Dependency[BaseModel]):
    def __init__(self, some_type: Type[BaseModel], *args, **kwargs):
        super().__init__(some_type, *args, **kwargs)

    def inject(self) -> BaseModel:
        from flask import request
        return self.some_type(**request.get_json())


def M(some_type):
    return ModelDependency(some_type)