import attrs

from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.common.pagination_dto import PaginationDTO
from todoapp.domain.services.todos.commands.add_todo import AddTodoCommand, AddTodoCommandHandler
from todoapp.domain.services.todos.commands.delete_todo import DeleteTodoCommand, DeleteTodoCommandHandler
from todoapp.domain.services.todos.commands.edit_todo import EditTodoCommand, EditTodoCommandHandler
from todoapp.domain.services.todos.queries.get_todo import GetTodoQuery, GetTodoQueryHandler
from todoapp.domain.services.todos.queries.get_todos import GetTodosQuery, GetTodosQueryHandler
from todoapp.domain.services.todos.todos_dtos import TodoDTO


@attrs.define
class TodosService:
    data_context: DataContext

    def add_todo(self, add_todo_command: AddTodoCommand) -> TodoDTO:
        return AddTodoCommandHandler(data_context=self.data_context).handle(command=add_todo_command)

    def edit_todo(self, edit_todo_command: EditTodoCommand) -> TodoDTO:
        return EditTodoCommandHandler(data_context=self.data_context).handle(command=edit_todo_command)

    def delete_todo(self, delete_todo_command: DeleteTodoCommand):
        DeleteTodoCommandHandler(data_context=self.data_context).handle(command=delete_todo_command)

    def get_todo(self, get_todo_query: GetTodoQuery) -> TodoDTO:
        return GetTodoQueryHandler(data_context=self.data_context).handle(command=get_todo_query)

    def get_todos(self, get_todos_query: GetTodosQuery) -> PaginationDTO:
        return GetTodosQueryHandler(data_context=self.data_context).handle(command=get_todos_query)
