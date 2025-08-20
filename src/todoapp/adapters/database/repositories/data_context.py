import attrs

from todoapp.adapters.database.repositories.todos_repository import TodosRepository
from todoapp.domain.repositories.todos_repository import AbstractTodosRepository


@attrs.define
class DataContext:
    todos_repo: AbstractTodosRepository = attrs.field(init=False)

    def __attrs_post_init__(self):
        self.todos_repo = TodosRepository()
