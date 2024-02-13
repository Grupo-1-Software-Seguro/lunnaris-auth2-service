from typing import TypeVar, Generic, Type
from abc import abstractmethod, ABC

T = TypeVar("T")


class Provider(Generic[T]):
    def key(self) -> Type[T]:
        pass

    def create(self) -> T:
        pass
