import uuid

import attrs
from sqlalchemy import select

from todoapp.adapters.app.dependencies import get_config, get_database_connector
from todoapp.adapters.database.database import DatabaseConnector
from todoapp.adapters.database.models import TodosORM, UsersORM
from todoapp.config import Config
from todoapp.domain.models.user import UserRole
from todoapp.domain.services.auth.auth import Auth

UUID_FIRST_USER = "521f2f68-b81c-4c83-b723-245d5b95e9b8"
UUID_FIRST_TODO = "d4755a43-84b4-4b28-abe9-15768df4f398"


@attrs.define
class Seed:
    database_connector: DatabaseConnector = attrs.field(init=False)
    config: Config

    def __attrs_post_init__(self):
        self.config = get_config()
        self.database_connector = get_database_connector(config=self.config)

    def seed(self):
        user_id = self.create_first_user()
        self.create_first_todo(user_id=user_id)

    def create_first_user(self) -> str:
        with self.database_connector.session_scope() as session:
            query = select(UsersORM).where(UsersORM.id == UUID_FIRST_USER)
            user_data = session.execute(query).scalar_one_or_none()

            if user_data is not None:
                return user_data

            (password, salt) = Auth.create_hashed_password_salt(self.config.admin_user_password)

            user = UsersORM(
                id=str(uuid.UUID(UUID_FIRST_USER)),
                email=self.config.admin_user_email,
                username="root",
                password=password,
                salt=salt,
                role=UserRole.ADMIN.value,
                is_active=True,
            )

            session.add(user)
            session.flush()
            return user.id

    def create_first_todo(self, user_id: str):
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
                owner_id=user_id,
            )

            session.add(todo)
            session.commit()
