import uuid

import attrs

from todoapp.domain.exceptions import NotFoundError
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.common.command_handler_base import CommandBase, CommandHandlerBase
from todoapp.domain.services.users.users_dtos import UserDTO


@attrs.define
class GetUserQuery(CommandBase):
    id: uuid.UUID


@attrs.define
class GetUserQueryHandler(CommandHandlerBase):
    data_context: DataContext

    def handle(self, command: GetUserQuery) -> UserDTO:
        user = self.data_context.users_repo.get_by_id(str(command.id))
        if not user:
            raise NotFoundError(f"User with id '{command.id}' does not exists")

        return UserDTO.from_model(user)
