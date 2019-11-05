from abc import ABCMeta, abstractmethod
from typing import List

from common.database import Database


class Model(metaclass=ABCMeta):
    @abstractmethod
    def json(self):
        raise NotImplementedError