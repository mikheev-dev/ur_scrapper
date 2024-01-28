from abc import ABC, abstractmethod


class BaseSaver(ABC):
    @abstractmethod
    def save(self, obj_repr: str):
        raise NotImplementedError

