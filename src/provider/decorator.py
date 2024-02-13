import inspect
from functools import wraps
from provider.service_provider import ProviderStore


def inject(fields=None):
    if fields is None:
        fields = []

    def super_function(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            parameters = inspect.signature(f).parameters
            for param in parameters.values():
                if param.name in fields:
                    kwargs[param.name] = ProviderStore().get(param.annotation)

            return f(*args, **kwargs)

        return decorated_function
    return super_function
