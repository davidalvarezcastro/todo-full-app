import attrs

from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.common.pagination_dto import PaginationDTO
from todoapp.domain.services.users.commands.add_user import AddUserCommand, AddUserCommandHandler
from todoapp.domain.services.users.commands.delete_user import DeleteUserCommand, DeleteUserCommandHandler
from todoapp.domain.services.users.commands.edit_user import EditUserCommand, EditUserCommandHandler
from todoapp.domain.services.users.queries.get_user import GetUserQuery, GetUserQueryHandler
from todoapp.domain.services.users.queries.get_users import GetUsersQuery, GetUsersQueryHandler
from todoapp.domain.services.users.users_dtos import UserDTO


@attrs.define
class UsersService:
    data_context: DataContext

    def add_user(self, add_user_command: AddUserCommand) -> UserDTO:
        return AddUserCommandHandler(data_context=self.data_context).handle(command=add_user_command)

    def edit_user(self, edit_user_command: EditUserCommand) -> UserDTO:
        return EditUserCommandHandler(data_context=self.data_context).handle(command=edit_user_command)

    def delete_user(self, delete_user_command: DeleteUserCommand):
        DeleteUserCommandHandler(data_context=self.data_context).handle(command=delete_user_command)

    def get_user(self, get_user_query: GetUserQuery) -> UserDTO:
        return GetUserQueryHandler(data_context=self.data_context).handle(command=get_user_query)

    def get_users(self, get_users_query: GetUsersQuery) -> PaginationDTO:
        return GetUsersQueryHandler(data_context=self.data_context).handle(command=get_users_query)
