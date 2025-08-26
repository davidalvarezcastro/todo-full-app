import attrs

from todoapp.adapters.database.database import DatabaseConnector
from todoapp.adapters.database.repositories.todos_repository import TodosRepository
from todoapp.adapters.database.repositories.users_repository import UsersRepository
from todoapp.domain.repositories.todos_repository import AbstractTodosRepository
from todoapp.domain.repositories.users_repository import AbstractUsersRepository


@attrs.define
class DataContext:
    database_connector: DatabaseConnector = attrs.field(init=True)
    todos_repo: AbstractTodosRepository = attrs.field(init=False)
    users_repo: AbstractUsersRepository = attrs.field(init=False)

    def __attrs_post_init__(self):
        self.todos_repo = TodosRepository(database_connector=self.database_connector)
        self.users_repo = UsersRepository(database_connector=self.database_connector)
