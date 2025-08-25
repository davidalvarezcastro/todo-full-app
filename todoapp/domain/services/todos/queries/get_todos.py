import attrs

from todoapp.domain.models.base_model import FiltersBase
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.common.command_handler_base import CommandHandlerBase, PaginationQueryBase
from todoapp.domain.services.common.pagination_dto import PaginationDTO
from todoapp.domain.services.todos.todos_dtos import TodoDTO


@attrs.define
class GetTodosQueryFilters(FiltersBase):
    priority: int | None = None


@attrs.define
class GetTodosQuery(PaginationQueryBase):
    filters: GetTodosQueryFilters | None = attrs.field(default=None)


@attrs.define
class GetTodosQueryHandler(CommandHandlerBase):
    data_context: DataContext

    def handle(self, command: GetTodosQuery) -> PaginationDTO:
        todos = self.data_context.todos_repo.get(
            filters=command.filters,
            order=command.order,
            order_by=command.order_by,
            offset=command.offset,
            limit=command.items,
        )

        total_items = self.data_context.todos_repo.count(filters=command.filters)
        todos_dto = [TodoDTO.from_model(todo) for todo in todos]
        return PaginationDTO(
            page=command.page,
            page_items=len(todos_dto),
            total_items=total_items,
            items=todos_dto,
        )
