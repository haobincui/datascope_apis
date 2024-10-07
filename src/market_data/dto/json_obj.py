from abc import ABC, abstractmethod


class JsonObj(ABC):

    @abstractmethod
    def to_json(self) -> dict:
        pass
