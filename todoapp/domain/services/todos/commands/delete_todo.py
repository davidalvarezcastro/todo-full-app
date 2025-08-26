import uuid

import attrs

from todoapp.domain.models.todo import Todo
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.common.command_handler_base import CommandBase, CommandHandlerBase


@attrs.define
class DeleteTodoCommand(CommandBase):
    id: uuid.UUID


@attrs.define
class DeleteTodoCommandHandler(CommandHandlerBase):
    data_context: DataContext

    def handle(self, command: DeleteTodoCommand):
        todo: Todo = self.data_context.todos_repo.get_by_id(id=str(command.id))
        if not todo:
            return

        self.data_context.todos_repo.delete(todo)
