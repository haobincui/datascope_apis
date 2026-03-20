from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.connection.extraction.enums.extraction_base_enums import IdentifierType


@dataclass()
class InstrumentIdentifierListBase(ABC):
    """
    abstract class for instrument identifier list
    """
    preferred_identifier_type: IdentifierType

    @abstractmethod
    def get_dict_form(self, request_name: str) -> dict:
        """Return dict form.

        Args:
            request_name (str): Input value for request name.

        Returns:
            dict: Requested value for the lookup.
        """
        pass


