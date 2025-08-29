from typing import TypeVar

import attrs

T = TypeVar("T")


@attrs.define
class PaginationDTO:
    page: int
    total_items: int
    page_items: int
    items: list[T]
