from datetime import datetime, timedelta

import pytest
from jose import jwt

from todoapp.domain.commons.date_utils import get_utc_now
from todoapp.domain.models.user import UserInfo
from todoapp.domain.services.auth.token import AbstractToken, JWTToken

SECRET = "supersecret"


@pytest.fixture
def token_handler() -> AbstractToken:
    return JWTToken(secret=SECRET)


def check_decoded_token_data(decoded_data: dict, user_data: UserInfo, expiration: datetime):
    assert decoded_data["user_id"] == user_data.user_id
    assert decoded_data["email"] == user_data.email
    assert decoded_data["roles"] == [role.value for role in user_data.roles]
    assert decoded_data["exp"] == int(expiration.timestamp())


class TestCreateToken:
    def test_token_contains_data(self, user_data, token_handler):
        expiration = get_utc_now() + timedelta(hours=1)

        token = token_handler.create_token(expiration_date=expiration, data=user_data.to_dict())
        decoded_data = jwt.decode(token, SECRET, algorithms=["HS256"])

        check_decoded_token_data(decoded_data=decoded_data, user_data=user_data, expiration=expiration)


class TestIsValidToken:
    def test_success_for_valid_token(self, user_data, token_handler):
        expiration = get_utc_now() + timedelta(hours=1)
        token = token_handler.create_token(expiration_date=expiration, data=user_data.to_dict())

        assert token_handler.is_valid_token(token) is True

    def test_fails_for_invalid_token(self, token_handler):
        invalid_token = "invalid.token.value"

        assert token_handler.is_valid_token(invalid_token) is False

    def test_fails_for_expired_token(self, user_data, token_handler):
        expiration = get_utc_now() - timedelta(hours=1)
        token = token_handler.create_token(expiration_date=expiration, data=user_data.to_dict())

        assert token_handler.is_valid_token(token) is False


class TestGetTokenData:
    def test_returns_correct_data(self, user_data, token_handler):
        expiration = get_utc_now() + timedelta(hours=1)
        token = token_handler.create_token(expiration_date=expiration, data=user_data.to_dict())

        decoded_data = token_handler.get_token_data(token)

        check_decoded_token_data(decoded_data=decoded_data, user_data=user_data, expiration=expiration)
