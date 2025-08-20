from typing import TypeVar

from pydantic import Field

from todoapp.adapters.app.controllers.common.conversion_api_domain import (
    ConversionAPIDomain,
)
from todoapp.domain.models.base_model import SortDirection

T = TypeVar("T")


class PaginationResultAPI[T](ConversionAPIDomain):
    page: int
    total_items: int
    page_items: int
    items: list[T]


class PaginationAPI(ConversionAPIDomain):
    order: SortDirection = SortDirection.NONE
    order_by: str | None = Field(default=None)
    page: int = Field(default=1, ge=1)
    items: int = Field(default=100, ge=1, le=100)


class PaginationFiltersAPI[T](PaginationAPI):
    filters: T | None = Field(default=None)
