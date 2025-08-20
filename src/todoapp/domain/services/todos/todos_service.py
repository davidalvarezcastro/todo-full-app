import attrs

from todoapp.adapters.database.repositories.data_context import DataContext
from todoapp.domain.services.common.pagination_dto import PaginationDTO
from todoapp.domain.services.todos.queries.get_todos import GetTodosQuery, GetTodosQueryHandler


@attrs.define
class TodosService:
    data_context: DataContext

    def get_todos(self, get_todos_query: GetTodosQuery) -> PaginationDTO:
        return GetTodosQueryHandler(data_context=self.data_context).handle(command=get_todos_query)
