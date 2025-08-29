import uuid
from unittest.mock import patch

import pytest

from todoapp.adapters.app.dependencies import get_config, get_database_connector, get_todos_service, get_users_service
from todoapp.adapters.database.database import DatabaseConnector
from todoapp.adapters.database.models import BaseORM
from todoapp.config import Config
from todoapp.domain.models.todo import Todo
from todoapp.domain.models.user import User, UserRole
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.todos.commands.add_todo import AddTodoCommand
from todoapp.domain.services.todos.todos_service import TodosService
from todoapp.domain.services.users.commands.add_user import AddUserCommand
from todoapp.domain.services.users.users_service import UsersService


@pytest.fixture(scope="function")
def config():
    return get_config()


@pytest.fixture(scope="function")
def db(config: Config) -> DatabaseConnector:
    database_connector = get_database_connector(config=config)

    BaseORM.metadata.drop_all(bind=database_connector.engine)
    BaseORM.metadata.create_all(bind=database_connector.engine)

    database_connector.migrate()

    return database_connector


@pytest.fixture(scope="function")
def datacontext(db) -> DataContext:
    return DataContext(database_connector=db)


@pytest.fixture(scope="function")
def users_service(datacontext) -> UsersService:
    return get_users_service(data_context=datacontext)


@pytest.fixture(scope="function")
def todos_service(datacontext) -> TodosService:
    return get_todos_service(data_context=datacontext)


@pytest.fixture
def users_data(users_service: UsersService) -> list[User]:
    users: list[User] = [
        User(
            id=str(uuid.UUID("f29e5787-efd2-4d56-b547-9c6595f4b372")),
            username="Admin 1",
            email="admin1@foo.com",
            password="f29e5787-efd2-4d56-b547-9c6595f4b372",
            role=UserRole.ADMIN,
            is_active=True,
        ),
        User(
            id=str(uuid.UUID("d2a09b40-9da4-4db7-8035-cd9a50a192fd")),
            username="User 1",
            email="user1@foo.com",
            password="d2a09b40-9da4-4db7-8035-cd9a50a192fd",
            role=UserRole.NORMAL,
            is_active=True,
        ),
        User(
            id=str(uuid.UUID("225294d5-778a-4ee3-badc-6b7f666fc6d8")),
            username="Admin 2",
            email="admin2@foo.com",
            password="225294d5-778a-4ee3-badc-6b7f666fc6d8",
            role=UserRole.ADMIN,
            is_active=True,
        ),
        User(
            id=str(uuid.UUID("b506879f-e5ed-49d0-8960-338fd266525e")),
            username="User 2",
            email="user2@foo.com",
            password="b506879f-e5ed-49d0-8960-338fd266525e",
            role=UserRole.NORMAL,
            is_active=True,
        ),
    ]

    for user in users:
        with patch("todoapp.domain.services.users.commands.add_user.uuid.uuid4") as uuid_faker:
            uuid_faker.return_value = user.id
            users_service.add_user(
                add_user_command=AddUserCommand(
                    email=user.email,
                    username=user.username,
                    password=user.password,
                    role=user.role,
                )
            )

    return users


@pytest.fixture
def todos_data(users_data: list[User], todos_service: TodosService) -> list[Todo]:
    todos: list[Todo] = []

    uuids = iter(
        [
            "1c0d3c74-1a4c-48a7-b7c0-88b6b62f0c1c",
            "63b1a5d7-6a3b-4a6d-9873-1f1e5d4c5e35",
            "f77a2c95-f038-4c02-84df-cc2e1b5b77ad",
            "4f48dbde-1f38-4ac7-a3c2-5595dc2e0b38",
        ]
    )

    for i, user in enumerate([user for user in users_data if user.role == UserRole.NORMAL]):
        todos.append(
            Todo(
                id=str(uuid.UUID(next(uuids))),
                title=f"title {i}",
                description=f"description {i}",
                priority=5 + i,
                completed=False,
                owner_id=str(user.id),
            ),
        )
        todos.append(
            Todo(
                id=str(uuid.UUID(next(uuids))),
                title=f"title {i} II",
                description=f"description {i} II",
                priority=5 + i,
                completed=False,
                owner_id=str(user.id),
            ),
        )

    for todo in todos:
        with patch("todoapp.domain.services.todos.commands.add_todo.uuid.uuid4") as uuid_faker:
            uuid_faker.return_value = todo.id
            add_todo_command = AddTodoCommand(
                title=todo.title,
                description=todo.description,
                priority=todo.priority,
            )
            add_todo_command.owner_id = todo.owner_id
            todos_service.add_todo(add_todo_command=add_todo_command)

    return todos


@pytest.fixture
def make_todo_for_user(todos_service: TodosService):
    def _make_todo_for_user(
        owner_id: str, *, todo_id: str | None = None, title: str = "title", description: str = "desc", priority: int = 5
    ) -> Todo:
        todo_id = todo_id or str(uuid.uuid4())
        todo = Todo(
            id=todo_id,
            title=title,
            description=description,
            priority=priority,
            completed=False,
            owner_id=owner_id,
        )

        # patch UUID so that the service generates the same id
        with patch("todoapp.domain.services.todos.commands.add_todo.uuid.uuid4") as uuid_faker:
            uuid_faker.return_value = todo.id
            add_todo_command = AddTodoCommand(
                title=todo.title,
                description=todo.description,
                priority=todo.priority,
            )
            add_todo_command.owner_id = owner_id
            todos_service.add_todo(add_todo_command=add_todo_command)

        return todo

    return _make_todo_for_user
