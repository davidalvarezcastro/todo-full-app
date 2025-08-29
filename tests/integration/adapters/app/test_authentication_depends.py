import uuid

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from todoapp.adapters.app.controllers.common.authorization import Authorization
from todoapp.domain.models.user import UserInfo, UserRole
from todoapp.domain.services.auth.token import AbstractToken

UUID_USER = uuid.UUID("521f2f68-b81c-4c83-b723-245d5b95e9b8")


class FakeTokenHandler(AbstractToken):
    def __init__(self, valid=True, refresh=False, roles=None):
        self.valid = valid
        self.refresh = refresh
        self.roles = roles or [UserRole.ADMIN]

    def is_valid_token(self, token: str) -> bool:
        return self.valid

    def get_token_data(self, token: str) -> dict:
        return {
            "user_id": str(UUID_USER),
            "username": "testuser",
            "roles": [r.value for r in self.roles],
            "is_refresh_token": self.refresh,
        }

    def create_token(self, data: dict, expires_delta=None) -> str:
        return "faketoken"

    def refresh_token(self, token: str) -> str:
        return "newfaketoken"


@pytest.fixture
def app():
    app = FastAPI()

    # ⚡ Override dependency
    def get_fake_token_handler():
        return FakeTokenHandler()

    app.dependency_overrides = {}
    from todoapp.adapters.app.dependencies import get_token_handler  # noqa: PLC0415

    app.dependency_overrides[get_token_handler] = get_fake_token_handler

    @app.get("/protected")
    def protected_route(user: UserInfo = Depends(Authorization([UserRole.ADMIN]))):  # noqa: B008
        return {"user": user.user_id}

    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestAuthenticationCustom:
    def test_protected_route_with_valid_token(self, client):
        response = client.get("/protected", headers={"Authorization": "Bearer sometoken"})
        assert response.status_code == 200
        assert response.json() == {"user": str(UUID_USER)}

    def test_protected_route_with_invalid_token(self, client, app):
        # override to make token invalid
        def get_invalid_token_handler():
            return FakeTokenHandler(valid=False)

        from todoapp.adapters.app.dependencies import get_token_handler  # noqa: PLC0415

        app.dependency_overrides[get_token_handler] = get_invalid_token_handler

        response = client.get("/protected", headers={"Authorization": "Bearer sometoken"})
        assert response.status_code == 401

    def test_protected_route_with_forbidden_role(self, client, app):
        def get_forbidden_token_handler():
            return FakeTokenHandler(valid=True, roles=[UserRole.NORMAL])

        from todoapp.adapters.app.dependencies import get_token_handler  # noqa: PLC0415

        app.dependency_overrides[get_token_handler] = get_forbidden_token_handler

        response = client.get("/protected", headers={"Authorization": "Bearer sometoken"})
        assert response.status_code == 403
