from abc import ABC, abstractmethod


class Feature(ABC):
    """
    abstract class for features in the database.
    """

    def to_obj(self):
        """
        data from the database is in the form of json. Therefore, need to deserialized to objective
        """
        raise NotImplementedError

    def to_json(self):
        """Convert to json.

        Returns:
            None: No value is returned.
        """
        raise NotImplementedError


