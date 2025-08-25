import uuid

import attrs

from todoapp.domain.exceptions import NotFoundError
from todoapp.domain.models.todos import Todo
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.common.command_handler_base import CommandBase, CommandHandlerBase
from todoapp.domain.services.todos.todos_dtos import TodoDTO


@attrs.define
class EditTodoCommand(CommandBase):
    id: uuid.UUID = attrs.field(init=False)
    description: str = attrs.field(validator=[attrs.validators.min_len(3)])
    priority: int = attrs.field(validator=[attrs.validators.gt(0), attrs.validators.le(10)])
    completed: bool = attrs.field()


@attrs.define
class EditTodoCommandHandler(CommandHandlerBase):
    data_context: DataContext

    def handle(self, command: EditTodoCommand) -> TodoDTO:
        todo: Todo = self.data_context.todos_repo.get_by_id(id=str(command.id))
        if not todo:
            raise NotFoundError(f"Todo with id '{command.id}' does not exists")

        if command.description is not None:
            todo.description = command.description
        if command.priority is not None:
            todo.priority = command.priority
        if command.completed is not None:
            todo.completed = command.completed

        todo = self.data_context.todos_repo.update(entity=todo)
        return TodoDTO.from_model(todo)
