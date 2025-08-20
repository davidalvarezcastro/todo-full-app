import uuid

import attrs

from todoapp.domain.models.base_model import BaseModel


@attrs.define
class Todo(BaseModel):
    title: str
    description: str
    priority: int
    owner_id: int  # FIXME: use user instance
    completed: bool = attrs.field(default=False)

    def __attrs_post_init__(self):
        self.id = str(uuid.uuid4())
