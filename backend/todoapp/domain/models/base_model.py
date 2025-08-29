from abc import ABC
from enum import IntEnum
from typing import TypeVar

T = TypeVar("T")


class BaseModel(ABC):
    id: T


class FiltersBase:
    def get_predicate(self):
        raise NotImplementedError("Extension predicate should be added in adapters/extensions/filters")


class SortDirection(IntEnum):
    NONE = 0
    ASC = 1
    DESC = 2
