import uuid

import attrs

from todoapp.domain.models.user import User
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.common.command_handler_base import CommandBase, CommandHandlerBase


@attrs.define
class DeleteUserCommand(CommandBase):
    id: uuid.UUID


@attrs.define
class DeleteUserCommandHandler(CommandHandlerBase):
    data_context: DataContext

    def handle(self, command: DeleteUserCommand):
        user: User = self.data_context.users_repo.get_by_id(str(command.id))
        if not user:
            return

        self.data_context.users_repo.delete(user)
