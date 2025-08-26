import uuid

from todoapp.adapters.app.controllers.common.conversion_api_domain import ConversionAPIDomain
from todoapp.domain.models.user import UserRole


class UserResultAPI(ConversionAPIDomain):
    id: uuid.UUID
    username: str
    email: str
    role: UserRole
