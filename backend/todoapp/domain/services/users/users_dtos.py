import uuid

import attrs

from todoapp.domain.models.user import UserRole
from todoapp.domain.services.todos.base_dto import BaseDTO


@attrs.define
class UserDTO(BaseDTO):
    id: uuid.UUID
    username: str
    email: str
    role: UserRole
