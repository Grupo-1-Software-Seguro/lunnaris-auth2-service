from functools import wraps
from pydantic import BaseModel
from flask import request
import inspect

class Validator:
    
    def validate(self, param: inspect.Parameter, _type, kwargs):
        if param.annotation == inspect._empty and _type != None:
            model = self.create_model(_type)
            kwargs[param.name] = model
        elif issubclass(param.annotation, BaseModel):
            model = self.create_model(param.annotation)
            kwargs[param.name] = model

    def create_model(self, _type):
        pass

class BodyValidator(Validator):
    
    def create_model(class_: BaseModel):
        content_type = request.headers.get("Content-Type")
        if content_type:
            if "application/json" in content_type:
                return class_(**request.get_json())
            elif "form-data" in content_type:
                return class_(**request.form)
            

class QueryValidator(Validator):
    
    def create_model(self, _type):
        args = self.get_args(request)
        return _type(**args)

    def get_args(self, request):
        parsed_args = {}
        for arg in request.args:
            values = request.args.getlist(arg)
            if len(values) == 1:
                parsed_args[arg] = values[0]
            elif len(values) > 1:
                parsed_args[arg] = values
        return parsed_args
    

def validate_with_models(body=None, query=None):
    def super_function(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            parameters = inspect.signature(f).parameters
            # Check if body exists
            if "body" in parameters:
                BodyValidator().validate(parameters["body"], body, kwargs)
            # Check if query exists
            if "query" in parameters:
                QueryValidator().validate(parameters["query"], query, kwargs)

            return f(*args, **kwargs)
        return decorated_function
    return super_function


