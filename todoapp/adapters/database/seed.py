import uuid

import attrs
from sqlalchemy import select

from todoapp.adapters.app.dependencies import get_config, get_database_connector
from todoapp.adapters.database.database import DatabaseConnector
from todoapp.adapters.database.models import TodosORM, UsersORM
from todoapp.config import Config

UUID_FIRST_TODO = "d4755a43-84b4-4b28-abe9-15768df4f398"


@attrs.define
class Seed:
    database_connector: DatabaseConnector = attrs.field(init=False)
    config: Config

    def __attrs_post_init__(self):
        self.config = get_config()
        self.database_connector = get_database_connector(config=self.config)

    def seed(self):
        self.create_first_todo()

    def create_first_user(self) -> UsersORM:
        pass

    def create_first_todo(self):
        with self.database_connector.session_scope() as session:
            query = select(TodosORM).where(TodosORM.id == UUID_FIRST_TODO)
            todo_data = session.execute(query).scalar_one_or_none()

            if todo_data is not None:
                return

            todo = TodosORM(
                id=str(uuid.UUID(UUID_FIRST_TODO)),
                title="Getting Used",
                description="This is a todo to get used to the system",
                priority=1,
                completed=False,
                owner_id=1,  # TODO: user-todo relationship
            )

            session.add(todo)
            session.commit()
