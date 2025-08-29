import uuid
from enum import Enum

import attrs

from todoapp.domain.models.base_model import BaseModel


class UserRole(Enum):
    NORMAL = 0
    ADMIN = 1


@attrs.define
class User(BaseModel):
    id: str
    username: str
    email: str
    password: str
    role: UserRole
    is_active: bool


@attrs.define
class UserInfo:
    user_id: str
    email: str
    roles: list[UserRole]

    def to_dict(self) -> dict:
        return {
            UserInfo.user_id.__name__: str(self.user_id),
            UserInfo.email.__name__: self.email,
            UserInfo.roles.__name__: [role.value for role in self.roles],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UserInfo":
        return UserInfo(
            user_id=str(uuid.UUID(data.get(UserInfo.user_id.__name__))),
            email=data.get(UserInfo.email.__name__),
            roles=[UserRole(role) for role in data.get(UserInfo.roles.__name__, [])],
        )

    def is_admin(self):
        return UserRole.ADMIN in self.roles
