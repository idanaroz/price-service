from abc import ABCMeta, abstractmethod
from typing import List, Dict, TypeVar, Type, Union

from common.database import Database

T = TypeVar('T', bound='Model')


class Model(metaclass=ABCMeta):
    collection: str
    _id: str

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

    def save_to_mongo(self):
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_to_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:
        return cls.find_one_by("_id", _id)

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})

        return [cls(**elem) for elem in elements_from_db]

    @classmethod
    def find_one_by(cls: Type[T], attribute: str,
                    value: Union[str, Dict]) -> T:  # Item.find_one_by('url', 'https://bla.com')
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[T], attribute, value: Union[str, Dict]) -> List[T]:
        return [cls(**elem) for elem in Database.find_one(cls.collection, {attribute: value})]
