import uuid

import attrs

from todoapp.domain.exceptions import ConflictError
from todoapp.domain.models.todo import Todo
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.common.command_handler_base import CommandBase, CommandHandlerBase
from todoapp.domain.services.todos.todos_dtos import TodoDTO


@attrs.define
class AddTodoCommand(CommandBase):
    title: str = attrs.field(validator=[attrs.validators.min_len(3)])
    description: str = attrs.field(validator=[attrs.validators.min_len(3)])
    priority: int = attrs.field(validator=[attrs.validators.gt(0), attrs.validators.le(10)])
    owner_id: uuid.UUID = attrs.field(init=False)


@attrs.define
class AddTodoCommandHandler(CommandHandlerBase):
    data_context: DataContext

    def handle(self, command: AddTodoCommand) -> TodoDTO:
        todo = self.data_context.todos_repo.get_by_title(title=command.title)
        if todo:
            raise ConflictError(f"Todo with title '{command.title}' already exists")

        todo = Todo(
            id=str(uuid.uuid4()),
            title=command.title,
            description=command.description,
            priority=command.priority,
            completed=False,
            owner_id=str(command.owner_id),
        )

        todo = self.data_context.todos_repo.add(entity=todo)

        return TodoDTO.from_model(todo)
