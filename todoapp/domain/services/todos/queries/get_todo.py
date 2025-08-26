import uuid

import attrs

from todoapp.domain.exceptions import NotFoundError
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.common.command_handler_base import CommandBase, CommandHandlerBase
from todoapp.domain.services.todos.todos_dtos import TodoDTO


@attrs.define
class GetTodoQuery(CommandBase):
    id: uuid.UUID


@attrs.define
class GetTodoQueryHandler(CommandHandlerBase):
    data_context: DataContext

    def handle(self, command: GetTodoQuery) -> TodoDTO:
        todo = self.data_context.todos_repo.get_by_id(id=str(command.id))

        if not todo:
            raise NotFoundError(f"Todo with id '{command.id}' does not exists")

        return TodoDTO.from_model(todo)
