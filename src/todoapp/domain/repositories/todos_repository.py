from abc import abstractmethod

from todoapp.adapters.database.repositories.repository_base import RepositoryBase
from todoapp.domain.models.todos import Todo


class AbstractTodosRepository(RepositoryBase[Todo]):
    @abstractmethod
    def get_by_owner_id(self, owner_id: int) -> Todo:
        """Retrieve todo by owner ID."""
        raise NotImplementedError
