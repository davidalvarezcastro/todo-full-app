import uuid
from unittest.mock import patch

import pytest

from todoapp.adapters.app.dependencies import get_config, get_database_connector, get_users_service
from todoapp.adapters.database.database import DatabaseConnector
from todoapp.adapters.database.models import BaseORM
from todoapp.config import Config
from todoapp.domain.models.user import User, UserRole
from todoapp.domain.repositories.data_context import DataContext
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
