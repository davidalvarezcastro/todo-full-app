import uuid

import attrs

from todoapp.domain.models.base_model import BaseModel


@attrs.define
class Todo(BaseModel):
    title: str
    description: str
    priority: int
    owner_id: str
    completed: bool = attrs.field(default=False)
    id: str = attrs.field(default=None)

    def __attrs_post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
