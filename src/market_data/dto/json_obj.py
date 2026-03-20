from abc import ABC, abstractmethod


class JsonObj(ABC):
    """Abstract interface for objects that can be serialized to JSON."""

    @abstractmethod
    def to_json(self) -> dict:
        """Convert to json.

        Returns:
            dict: Computed result of the operation.
        """
        pass
