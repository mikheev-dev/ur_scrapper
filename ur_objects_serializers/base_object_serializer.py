from abc import ABC, abstractmethod
from typing import Any


class BaseSerializer(ABC):
    @abstractmethod
    def serialize(self, obj: Any) -> str:
        raise NotImplementedError
