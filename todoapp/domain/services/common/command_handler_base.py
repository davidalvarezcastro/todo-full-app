from abc import ABC, abstractmethod
from typing import TypeVar

import attrs

from todoapp.domain.models.base_model import SortDirection

T = TypeVar("T")


@attrs.define
class CommandBase:
    pass


@attrs.define
class PaginationQueryBase(CommandBase):
    order: SortDirection = SortDirection.NONE
    order_by: str | None = None
    page: int = attrs.field(default=1, validator=[attrs.validators.ge(1)])
    items: int = attrs.field(default=100, validator=[attrs.validators.ge(1), attrs.validators.le(100)])

    @property
    def offset(self):
        return (self.page - 1) * self.items


@attrs.define
class CommandHandlerBase(ABC):
    @abstractmethod
    def handle(self, command: CommandBase) -> T:
        pass
