from typing import TypeVar, Generic

T = TypeVar("T")


class DataTab(Generic[T]):
    def set_data(self, data: T) -> None:
        raise NotImplementedError
