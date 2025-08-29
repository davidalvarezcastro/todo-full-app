import uuid

import pytest
from fastapi import HTTPException

from todoapp.adapters.app.controllers.common.authorization import Authorization
from todoapp.domain.models.user import UserInfo, UserRole

UUID_USER = uuid.UUID("521f2f68-b81c-4c83-b723-245d5b95e9b8")


class DummyTokenHandler:
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
            "roles": [r.value for r in self.roles],  # depende cómo serialices UserRole
            "is_refresh_token": self.refresh,
        }


def make_credentials(token: str = "valid"):
    from fastapi.security import HTTPAuthorizationCredentials

    return HTTPAuthorizationCredentials(scheme="bearer", credentials=token)


class TestAuthenticationCustom:
    def test_valid_token_and_role(self):
        auth = Authorization(allowerd_roles=[UserRole.ADMIN])
        handler = DummyTokenHandler(valid=True, refresh=False, roles=[UserRole.ADMIN])
        creds = make_credentials()

        user = auth._validate_token_and_roles(handler, creds)

        assert isinstance(user, UserInfo)
        assert user.user_id == str(UUID_USER)
        assert UserRole.ADMIN in user.roles

    def test_invalid_scheme(self):
        auth = Authorization()
        handler = DummyTokenHandler()
        from fastapi.security import HTTPAuthorizationCredentials

        creds = HTTPAuthorizationCredentials(scheme="basic", credentials="token")

        with pytest.raises(HTTPException) as exc:
            auth._validate_token_and_roles(handler, creds)
        assert exc.value.status_code == 401

    def test_invalid_token(self):
        auth = Authorization()
        handler = DummyTokenHandler(valid=False)
        creds = make_credentials()

        with pytest.raises(HTTPException) as exc:
            auth._validate_token_and_roles(handler, creds)
        assert exc.value.status_code == 401

    def test_refresh_token_rejected(self):
        auth = Authorization()
        handler = DummyTokenHandler(valid=True, refresh=True)
        creds = make_credentials()

        with pytest.raises(HTTPException) as exc:
            auth._validate_token_and_roles(handler, creds)
        assert exc.value.status_code == 401

    def test_user_without_required_role(self):
        auth = Authorization(allowerd_roles=[UserRole.ADMIN])
        handler = DummyTokenHandler(valid=True, roles=[UserRole.NORMAL])
        creds = make_credentials()

        with pytest.raises(HTTPException) as exc:
            auth._validate_token_and_roles(handler, creds)
        assert exc.value.status_code == 403
