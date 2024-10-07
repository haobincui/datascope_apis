from abc import ABC, abstractmethod


class Feature(ABC):
    """
    abstract class for features in the database.
    """

    def to_obj(self):
        """
        data from the database is in the form of json. Therefore, need to deserialized to objective
        """
        pass

    def to_json(self):
        pass



