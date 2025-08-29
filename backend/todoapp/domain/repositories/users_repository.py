from abc import abstractmethod

from todoapp.domain.models.user import User
from todoapp.domain.repositories.repository_base import AbstractRepository


class AbstractUsersRepository(AbstractRepository):
    @abstractmethod
    def get_by_email(self, email: str) -> User:
        """Retrieve user by email."""
        raise NotImplementedError
