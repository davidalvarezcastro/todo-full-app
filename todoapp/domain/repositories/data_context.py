import attrs

from todoapp.adapters.database.database import DatabaseConnector
from todoapp.adapters.database.repositories.todos_repository import TodosRepository
from todoapp.domain.repositories.todos_repository import AbstractTodosRepository


@attrs.define
class DataContext:
    database_connector: DatabaseConnector = attrs.field(init=True)
    todos_repo: AbstractTodosRepository = attrs.field(init=False)

    def __attrs_post_init__(self):
        self.todos_repo = TodosRepository(database_connector=self.database_connector)
