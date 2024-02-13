from typing import TypeVar, Type
from exceptions import NotRegisteredType
from .provided_object import Provider


T = TypeVar("T")


class SingletonMeta(type):
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


class ProviderStore(metaclass=SingletonMeta):

    objects: dict

    def __init__(self):
        self.objects = {}

    def set(self, obj: T):
        self.objects[type(T)] = obj

    def set_callable(self, _type: Type[T], obj):
        if callable(obj):
            self.objects[_type] = obj

    def get(self, _type: Type[T]) -> T:
        if _type not in self.objects:
            raise NotRegisteredType(_type)

        obj = self.objects.get(_type)
        if callable(obj):
            return obj()

        return obj

