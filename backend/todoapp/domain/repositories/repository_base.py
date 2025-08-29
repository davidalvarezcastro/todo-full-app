import uuid
from abc import ABC, abstractmethod
from typing import TypeVar

from todoapp.domain.models.base_model import FiltersBase, SortDirection

T = TypeVar("T")
K = TypeVar("K", int, str, uuid.UUID)


class AbstractRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: K) -> T:  # noqa: A002
        pass

    @abstractmethod
    def get(
        self,
        join_types: list[T] | None = None,
        filters: FiltersBase | None = None,
        order: SortDirection = SortDirection.NONE,
        order_by: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[T]:
        pass

    @abstractmethod
    def count(
        self,
        join_types: list[T] | None = None,
        filters: FiltersBase | None = None,
    ) -> int:
        pass
