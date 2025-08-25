import uuid

from todoapp.adapters.app.controllers.common.conversion_api_domain import ConversionAPIDomain


class TodoResultAPI(ConversionAPIDomain):
    id: uuid.UUID
    title: str
    description: str
    priority: int
    completed: bool
