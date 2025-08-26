import attrs
from sqlalchemy import select

from todoapp.adapters.database.database import DatabaseConnector
from todoapp.adapters.database.models import UsersORM
from todoapp.adapters.database.repositories.repository_base import RepositoryBase
from todoapp.domain.models.user import User, UserRole
from todoapp.domain.repositories.users_repository import AbstractUsersRepository


@attrs.define
class UsersRepository(RepositoryBase[UsersORM], AbstractUsersRepository):
    database_connector: DatabaseConnector

    def _orm_to_domain_model(self, entity_orm: UsersORM) -> User:
        return User(
            id=str(entity_orm.id),
            username=entity_orm.username,
            email=entity_orm.email,
            password=entity_orm.password,
            salt=entity_orm.salt,
            role=UserRole(entity_orm.role),
            is_active=entity_orm.is_active,
        )

    def _domain_model_to_orm(self, entity_model: User) -> UsersORM:
        return UsersORM(
            id=str(entity_model.id),
            email=entity_model.email,
            username=entity_model.username,
            password=entity_model.password,
            salt=entity_model.salt,
            role=entity_model.role.value,
            is_active=entity_model.is_active,
        )

    def get_by_email(self, email: str) -> User:
        with self.database_connector.session_scope() as session:
            query = select(UsersORM).where(UsersORM.email == email)
            user_orm = session.execute(query).scalar_one_or_none()
            return self._orm_to_domain_model(user_orm) if user_orm else None
