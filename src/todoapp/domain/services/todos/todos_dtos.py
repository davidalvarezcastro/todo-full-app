import uuid

import attrs

from todoapp.domain.services.todos.base_dto import BaseDTO


@attrs.define
class TodoDTO(BaseDTO):
    id: uuid.UUID | None
    title: str
    description: str
    priority: int
    owner_id: int
    completed: bool = attrs.field(default=False)
