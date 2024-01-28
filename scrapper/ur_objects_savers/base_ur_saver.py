from abc import ABC, abstractmethod


class BaseSaver(ABC):
    """
    Class for saving the representation of an object
    """
    @abstractmethod
    def save(self, obj_repr: str):
        raise NotImplementedError

