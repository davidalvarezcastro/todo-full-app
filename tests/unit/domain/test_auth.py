import uuid
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import pytest

from todoapp.domain.exceptions import UnauthorizedError
from todoapp.domain.models.user import User, UserRole
from todoapp.domain.services.auth.auth import Auth
from todoapp.domain.services.auth.auth_dtos import AuthTokenResultDTO, LoginDTO

if TYPE_CHECKING:
    from todoapp.config import Config
    from todoapp.domain.repositories.data_context import DataContext
    from todoapp.domain.services.auth.token import AbstractToken


USER_ID = str(uuid.uuid4())
PASSWORD = "secret"
EMAIL = "davalv@televes.com"


@pytest.fixture
def mock_user() -> User:
    return User(
        id=USER_ID,
        username="davalv",
        email=EMAIL,
        password=Auth.create_hashed_password(PASSWORD),
        role=UserRole.NORMAL,
        is_active=True,
    )


@pytest.fixture
def mock_data_context(mock_user) -> "DataContext":
    repo = MagicMock()
    repo.get_by_email.return_value = mock_user
    data_context = MagicMock()
    data_context.users_repo = repo
    return data_context


@pytest.fixture
def mock_config() -> "Config":
    class DummyConfig:
        jwt_token_expiration_seconds = 3600
        jwt_refresh_token_expiration_seconds = 7200

    return DummyConfig()


@pytest.fixture
def mock_token_handler() -> "AbstractToken":
    handler = MagicMock()
    handler.create_token.side_effect = lambda _, data: f"TOKEN-{data['user_id']}"
    handler.is_valid_token.return_value = True
    handler.get_token_data.side_effect = lambda _: {
        "user_id": USER_ID,
        "email": EMAIL,
        "roles": [UserRole.NORMAL.value],
    }
    return handler


@pytest.fixture
def auth_service(mock_data_context, mock_config, mock_token_handler):
    return Auth(
        data_context=mock_data_context,
        config=mock_config,
        token_handler=mock_token_handler,
    )


def test_login_success(auth_service, mock_user, mock_token_handler):
    login_data = LoginDTO(email=mock_user.email, password=PASSWORD)

    result: AuthTokenResultDTO = auth_service.login(login_data)

    assert isinstance(result, AuthTokenResultDTO)
    # we do not care about the generated token
    assert result.token.startswith("TOKEN-")
    assert result.refresh_token.startswith("TOKEN-")
    mock_token_handler.create_token.assert_called()


def test_login_invalid_email(auth_service, mock_data_context):
    mock_data_context.users_repo.get_by_email.return_value = None
    login_data = LoginDTO(email="notfound@example.com", password=PASSWORD)

    with pytest.raises(UnauthorizedError):
        auth_service.login(login_data)


def test_login_invalid_password(auth_service, mock_data_context, mock_user):
    mock_user.password = Auth.create_hashed_password("anotherpassword")
    login_data = LoginDTO(email=mock_user.email, password="wrong")

    with pytest.raises(UnauthorizedError):
        auth_service.login(login_data)


def test_refresh_success(auth_service, mock_token_handler):
    mock_token_handler.is_valid_token.return_value = True
    fake_token = "validtoken"

    result: AuthTokenResultDTO = auth_service.refresh(fake_token)

    assert isinstance(result, AuthTokenResultDTO)
    # checking if a new token was generated
    assert result.token.startswith("TOKEN-")
    assert result.refresh_token.startswith("TOKEN-")
    mock_token_handler.create_token.assert_called()


def test_refresh_invalid_token(auth_service, mock_token_handler):
    mock_token_handler.is_valid_token.return_value = False
    fake_token = "badtoken"

    with pytest.raises(UnauthorizedError):
        auth_service.refresh(fake_token)


def test_password_hashing_and_checking():
    password = "supersecret"
    hashed = Auth.create_hashed_password(password)

    assert Auth.check_password(password, hashed) is True
    assert Auth.check_password("wrongpassword", hashed) is False
