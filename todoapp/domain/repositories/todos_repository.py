from abc import abstractmethod

from todoapp.domain.models.todos import Todo
from todoapp.domain.repositories.repository_base import AbstractRepository


class AbstractTodosRepository(AbstractRepository):
    @abstractmethod
    def get_by_owner_id(self, owner_id: int) -> Todo:
        """Retrieve todo by owner ID."""
        raise NotImplementedError

    @abstractmethod
    def get_by_title(self, title: str) -> Todo:
        """Retrieve todo by title."""
        raise NotImplementedError
