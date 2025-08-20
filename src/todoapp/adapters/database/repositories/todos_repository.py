import attrs
from sqlalchemy import select

from todoapp.adapters.database.database import DatabaseConnector
from todoapp.adapters.database.models import TodosORM
from todoapp.domain.models.todos import Todo
from todoapp.domain.repositories.todos_repository import AbstractTodosRepository


@attrs.define
class TodosRepository(AbstractTodosRepository):
    database_connector: DatabaseConnector

    def _orm_to_domain_model(self, entity_orm: TodosORM) -> Todo:
        return Todo(
            title=entity_orm.title,
            description=entity_orm.description,
            priority=entity_orm.priority,
            completed=entity_orm.completed,
            owner_id=-1,
        )

    def _domain_model_to_orm(self, entity_model: Todo) -> TodosORM:
        return TodosORM(
            id=str(entity_model.id),
            title=entity_model.title,
            description=entity_model.description,
            priority=entity_model.priority,
            completed=entity_model.completed,
            owner_id=-1,
        )

    def get_by_owner_id(self, owner_id: int) -> Todo:
        with self.database_connector.session_scope() as session:
            query = select(TodosORM).where(TodosORM.owner_id == owner_id)
            todo_orm = session.execute(query).scalar_one_or_none()
            return self._orm_to_domain_model(todo_orm) if todo_orm else None
