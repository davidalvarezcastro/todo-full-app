import os
import uuid
from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient

from todoapp.domain.commons.date_utils import to_iso_format_with_z
from todoapp.domain.services.auth.token import JWTToken
from todoapp.domain.services.users.users_dtos import UserDTO


def is_valid_token(login_data: dict, fake_datetime: datetime, fake_user: UserDTO):
    expected_token_expiration_date: datetime = fake_datetime + timedelta(
        seconds=int(os.getenv("JWT_TOKEN_EXPIRATION_SECONDS"))
    )
    expected_refresh_token_expiration_date: datetime = fake_datetime + timedelta(
        seconds=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRATION_SECONDS"))
    )

    assert "token" in login_data
    assert "refresh_token" in login_data
    assert "token_expiration_date" in login_data
    assert "refresh_token_expiration_date" in login_data
    assert login_data["token_expiration_date"] == to_iso_format_with_z(expected_token_expiration_date)  # fastapi format
    assert login_data["refresh_token_expiration_date"] == to_iso_format_with_z(
        expected_refresh_token_expiration_date
    )  # fastapi format

    token_handler = JWTToken(secret=os.getenv("JWT_SECRET"), ending_algorithm="HS256")
    assert token_handler.is_valid_token(login_data["token"]) is True
    decoded_token = token_handler.get_token_data(login_data["token"])
    assert str(uuid.UUID(decoded_token["user_id"])) == fake_user.id
    assert decoded_token["email"] == fake_user.email


class TestLogin:
    def test_success_valid_token_when_valid_data(self, user_admin_mock: UserDTO, client: Generator[TestClient]):
        with patch("todoapp.domain.services.auth.auth.get_utc_now") as get_utc_now_mock:
            fake_user, fake_password = user_admin_mock
            fake_datetime = datetime(2500, 2, 12, 8, 0, 0).astimezone(tz=UTC)
            get_utc_now_mock.return_value = fake_datetime

            response = client.post("/auth/login", json={"email": fake_user.email, "password": fake_password})

            assert response.status_code == status.HTTP_200_OK
            login_data = response.json()

            is_valid_token(login_data=login_data, fake_datetime=fake_datetime, fake_user=fake_user)

    def test_fail_when_invalid_password(self, user_admin_mock, client: Generator[TestClient]):
        fake_user, _ = user_admin_mock
        response = client.post("/auth/login", json={"email": fake_user.email, "password": "sdasd"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["details"]["msg"] == "Invalid credentials. Please check your username and password."


class TestRefreshToken:
    def test_success_valid_token_when_valid_refresh_token(self, user_admin_mock, client: Generator[TestClient]):
        fake_user, fake_password = user_admin_mock

        # log in to get a refresh token, if this endpoints is incorrect, the previous tests will fail
        login_response = client.post("/auth/login", json={"email": fake_user.email, "password": fake_password})
        assert login_response.status_code == 200
        login_data = login_response.json()

        with patch("todoapp.domain.services.auth.auth.get_utc_now") as get_utc_now_mock:
            fake_datetime = datetime(2500, 2, 12, 8, 0, 0).astimezone(tz=UTC)
            get_utc_now_mock.return_value = fake_datetime
            refresh_token = login_data["refresh_token"]
            refresh_response = client.post(f"/auth/refresh?refresh_token={refresh_token}")

            assert refresh_response.status_code == status.HTTP_200_OK
            refresh_data = refresh_response.json()

            is_valid_token(login_data=refresh_data, fake_datetime=fake_datetime, fake_user=fake_user)

    def test_fail_when_invalid_refresh_token(self, client: Generator[TestClient]):
        invalid_refresh_token = "invalid.token.string"
        response = client.post(f"/auth/refresh?refresh_token={invalid_refresh_token}")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["details"]["msg"] == "Invalid refresh token."

    def test_fail_when_expired_refresh_token(self, user_admin_mock, client: Generator[TestClient]):
        with patch("todoapp.domain.services.auth.auth.get_utc_now") as get_utc_now_mock:
            fake_datetime = datetime(2025, 2, 12, 8, 0, 0).astimezone(tz=UTC)
            get_utc_now_mock.return_value = fake_datetime
            fake_user, fake_password = user_admin_mock

            login_response = client.post("/auth/login", json={"email": fake_user.email, "password": fake_password})
            assert login_response.status_code == status.HTTP_200_OK
            login_data = login_response.json()

            refresh_token = login_data["refresh_token"]
            refresh_response = client.post(f"/auth/refresh?refresh_token={refresh_token}")

            assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED
            assert refresh_response.json()["details"]["msg"] == "Invalid refresh token."
