import attrs

from todoapp.domain.models.base_model import FiltersBase
from todoapp.domain.models.user import UserRole
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.common.command_handler_base import CommandHandlerBase, PaginationQueryBase
from todoapp.domain.services.common.pagination_dto import PaginationDTO
from todoapp.domain.services.users.users_dtos import UserDTO


@attrs.define
class GetUsersQueryFilters(FiltersBase):
    username: str | None = attrs.field(default=None)
    email: str | None = attrs.field(default=None)
    roles: list[UserRole] | None = attrs.field(default=None)


@attrs.define
class GetUsersQuery(PaginationQueryBase):
    filters: GetUsersQueryFilters | None = attrs.field(default=None)


@attrs.define
class GetUsersQueryHandler(CommandHandlerBase):
    data_context: DataContext

    def handle(self, command: GetUsersQuery) -> PaginationDTO:
        users = self.data_context.users_repo.get(
            filters=command.filters,
            order=command.order,
            order_by=command.order_by,
            offset=command.offset,
            limit=command.items,
        )
        total_items = self.data_context.users_repo.count(filters=command.filters)

        users_dto = [UserDTO.from_model(user) for user in users]
        return PaginationDTO(page=command.page, page_items=len(users_dto), total_items=total_items, items=users_dto)
