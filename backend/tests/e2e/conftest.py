import uuid
from collections.abc import Generator
from unittest.mock import patch

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from todoapp.adapters.app.controllers.auth.auth_controller import AuthTokenResultAPI
from todoapp.domain.models.user import UserRole
from todoapp.domain.services.users.commands.add_user import AddUserCommand
from todoapp.domain.services.users.users_dtos import UserDTO

load_dotenv(".env.testing", override=True)


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    from todoapp.adapters.app.app import create_app  # noqa: PLC0415

    app = create_app()
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
@patch("todoapp.domain.services.users.commands.add_user.uuid.uuid4")
def user_admin_mock(uuid1, users_service) -> tuple[UserDTO, str]:
    fake_password = "fake_password"
    uuid_fake_user_tenant = uuid.UUID("521f2f68-b81c-4c83-b723-245d5b95e9b8")
    uuid1.return_value = uuid_fake_user_tenant
    add_user_command = AddUserCommand(
        username="admintodoapp",
        email="fake@todoapp.com",
        password=fake_password,
        role=UserRole.ADMIN,
    )
    user = users_service.add_user(add_user_command=add_user_command)

    return (user, fake_password)


@pytest.fixture(scope="function")
@patch("todoapp.domain.services.users.commands.add_user.uuid.uuid4")
def user_normal_mock(uuid1, users_service) -> tuple[UserDTO, str]:
    fake_password = "fake_password"
    uuid_fake_user_tenant = uuid.UUID("4e39ec54-ad8b-4b3d-b973-a25325e3675a")
    uuid1.return_value = uuid_fake_user_tenant
    add_user_command = AddUserCommand(
        username="normaluser",
        email="normaluser@todoapp.com",
        password=fake_password,
        role=UserRole.NORMAL,
    )
    user = users_service.add_user(add_user_command=add_user_command)

    return (user, fake_password)


@pytest.fixture(scope="function")
def authorization_admin_header(user_admin_mock, client: Generator[TestClient]) -> Generator[TestClient]:
    user, fake_password = user_admin_mock
    response = client.post("/auth/login", json={"email": user.email, "password": fake_password})
    auth_token = AuthTokenResultAPI(**response.json())
    return {"Authorization": f"Bearer {auth_token.token}"}


@pytest.fixture(scope="function")
def authorization_normal_header(user_normal_mock, client: Generator[TestClient]) -> Generator[TestClient]:
    user, fake_password = user_normal_mock
    response = client.post("/auth/login", json={"email": user.email, "password": fake_password})
    auth_token = AuthTokenResultAPI(**response.json())
    return {"Authorization": f"Bearer {auth_token.token}"}
