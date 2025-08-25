import uuid
from abc import abstractmethod
from typing import Generic, TypeVar, get_args, get_origin

import attrs
from sqlalchemy import Select, Tuple, asc, desc, func, select, update

from todoapp.adapters.database.database import DatabaseConnector
from todoapp.adapters.database.models import BaseORM
from todoapp.domain.models.base_model import BaseModel, FiltersBase, SortDirection
from todoapp.domain.repositories.repository_base import AbstractRepository

T = TypeVar("T", bound=BaseModel)
K = TypeVar("K", bound=BaseORM)
G = TypeVar("G", int, uuid.UUID)


@attrs.define
class RepositoryBase[T](AbstractRepository):
    # IMPORTANT: We need to repeat properties in child classes
    # in order to constructor class work because it is a limitation of attr library
    database_connector: DatabaseConnector

    @abstractmethod
    def _orm_to_domain_model(self, entity_orm: K) -> T:
        pass

    @abstractmethod
    def _domain_model_to_orm(self, entity_model: T) -> K:
        pass

    @property
    def orm_cls(self):
        bases = self.__class__.__orig_bases__  # The generic bases

        for base in bases:
            if get_origin(base) is RepositoryBase:
                args = get_args(base)
                if args:
                    return args[0]  # The T in RepositoryBase[T]

        raise TypeError("Repository should extend RepositoryBase[OrmEntity] as Generic[T]")

    def get_by_id(self, id: Generic[G]) -> T:  # noqa: A002
        with self.database_connector.session_scope() as session:
            entity_orm = session.get(self.orm_cls, id)
            return self._orm_to_domain_model(entity_orm) if entity_orm else None

    def add(self, entity: T) -> T:
        with self.database_connector.session_scope() as session:
            entity_orm = self._domain_model_to_orm(entity)
            session.add(entity_orm)
            session.flush()

            return self._orm_to_domain_model(entity_orm)

    def delete(self, entity: T):
        with self.database_connector.session_scope() as session:
            entity_orm = session.get(self.orm_cls, entity.id)
            session.delete(entity_orm)

    def update(self, entity: T) -> T:
        entity_orm = self._domain_model_to_orm(entity)
        with self.database_connector.session_scope() as session:
            session.execute(update(self.orm_cls), [entity_orm.__dict__])

        return self.get_by_id(entity.id)

    def get(
        self,
        join_types: list[T] | None = None,
        filters: FiltersBase | None = None,
        order: SortDirection = SortDirection.NONE,
        order_by: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[T]:
        query = select(self.orm_cls).select_from(self.orm_cls)
        query = self._generate_query_joins_filters(query, join_types, filters)

        if order_by:
            order_field = getattr(self.orm_cls, order_by, None)

        if order and order_field:
            query = query.order_by(asc(order_field) if order == SortDirection.ASC else desc(order_field))

        if offset:
            query = query.offset(offset)

        if limit:
            query = query.limit(limit)

        with self.database_connector.session_scope() as session:
            entities_orm = session.execute(query).scalars()
            return [self._orm_to_domain_model(entity_orm) for entity_orm in entities_orm]

    def count(
        self,
        join_types: list[T] | None = None,
        filters: FiltersBase | None = None,
    ) -> int:
        query = select(func.count("*")).select_from(self.orm_cls)
        query = self._generate_query_joins_filters(query, join_types, filters)

        with self.database_connector.session_scope() as session:
            return session.execute(query).scalar()

    def _generate_query_joins_filters(
        self,
        query: Select[Tuple],
        join_types: list[T] | None = None,
        filters: FiltersBase | None = None,
    ) -> Select[Tuple]:
        # TODO: See if we can put in global imports because it produce a problem with circular imports
        import todoapp.adapters.database.extensions  # noqa: F401, PLC0415

        if not join_types:
            join_types = []

        for join in join_types:
            query = query.join(join.orm_cls)

        filters_predicate = None
        if filters:
            filters_predicate = filters.get_predicate()

        if filters_predicate is not None:
            query = query.where(filters_predicate)

        return query
