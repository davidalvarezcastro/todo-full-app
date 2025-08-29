import uuid

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from todoapp.adapters.app.controllers.common.pagination_api import PaginationResultAPI
from todoapp.adapters.app.controllers.users.user_result_api import UserResultAPI
from todoapp.domain.models.user import User, UserRole
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.auth.auth import Auth
from todoapp.domain.services.users.users_dtos import UserDTO


class TestAddUserAPI:
    def test_creates_user_when_valid_data(
        self, authorization_admin_header, datacontext: DataContext, client: TestClient
    ):
        user_request_body = {"username": "fakeuser", "email": "fake@user.com", "password": "12345678", "role": 0}
        response = client.post("/user/", headers=authorization_admin_header, json=user_request_body)
        assert response.status_code == status.HTTP_201_CREATED

        user_result = UserResultAPI(**response.json())
        assert user_result.username == user_request_body["username"]
        assert user_result.email == user_request_body["email"]
        assert user_result.role == UserRole(user_request_body["role"])

        user: User = datacontext.users_repo.get_by_id(id=str(user_result.id))
        assert user
        assert user.username == user_request_body["username"]
        assert user.email == user_request_body["email"]
        assert user.role == UserRole(user_request_body["role"])
        assert Auth.check_password(plain_password=user_request_body["password"], hashed_password=user.password)

    def test_add_exiting(self, authorization_admin_header, users_data: list[User], client: TestClient):
        existing_user = users_data[0]
        user_request_body = {
            "username": existing_user.username,
            "email": existing_user.email,
            "password": "12345678",
            "role": 0,
        }
        response = client.post("/user/", headers=authorization_admin_header, json=user_request_body)
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.parametrize(
        "username, email, password, role",
        [
            ("fa", "fake@user.com", "12345678", 0),
            ("fake user", "fakxcvxcxcv@czxczx", "12345678", 0),
            ("fake user", "fake@user.com", "12", 0),
            ("fake user", "fake@user.com", "12345678", 4),
        ],
    )
    def test_add_validation_error(
        self, username: str, email: str, password: str, role: int, authorization_admin_header, client: TestClient
    ):
        user_request_body = {"username": username, "email": email, "password": password, "role": role}
        response = client.post("/user/", headers=authorization_admin_header, json=user_request_body)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestEditUserAPI:
    @pytest.mark.parametrize(
        "email, password",
        [("fake@user.com", "asdfghjkl"), ("other@other.com", None)],
    )
    def test_edit_success(
        self,
        email: str,
        password: str,
        authorization_admin_header,
        datacontext: DataContext,
        users_data: list[User],
        client: TestClient,
    ):
        existing_user = users_data[1]
        user_request_body = {
            "email": email,
            "password": password,
        }
        response = client.put(f"/user/{existing_user.id}", headers=authorization_admin_header, json=user_request_body)
        assert response.status_code == status.HTTP_200_OK

        user_result = UserResultAPI(**response.json())
        assert str(user_result.id) == existing_user.id
        assert user_result.email == user_request_body["email"]

        user: User = datacontext.users_repo.get_by_id(id=str(user_result.id))
        assert user
        assert user.email == user_request_body["email"]
        if password is not None:
            assert Auth.check_password(plain_password=user_request_body["password"], hashed_password=user.password)

    @pytest.mark.parametrize(
        "username, email, password, role",
        [
            ("fa", "fake@user.com", "12345678", 0),
            ("fake user", "fakxcvxcxcv@czxczx", "12345678", 0),
            ("fake user", "fake@user.com", "12", 0),
            ("fake user", "fake@user.com", "asdsafas", 4),
        ],
    )
    def test_edit_validation_error(
        self, username: str, email: str, password: str, role: int, authorization_admin_header, client: TestClient
    ):
        user_request_body = {"username": username, "email": email, "password": password, "role": role}
        response = client.post("/user/", headers=authorization_admin_header, json=user_request_body)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestDeleteUserAPI:
    def test_delete_success(
        self, authorization_admin_header, users_data: list[User], datacontext: DataContext, client: TestClient
    ):
        existing_user = users_data[0]
        response = client.delete(f"/user/{existing_user.id}", headers=authorization_admin_header)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        user: User = datacontext.users_repo.get_by_id(existing_user.id)
        assert user is None


class TestGetUserAPI:
    def test_get_success(self, authorization_admin_header, users_data: list[User], client: TestClient):
        existing_user = users_data[0]
        response = client.get(f"/user/{existing_user.id}", headers=authorization_admin_header)
        assert response.status_code == status.HTTP_200_OK

        user_api: UserResultAPI = UserResultAPI(**response.json())
        assert str(user_api.id) == existing_user.id
        assert user_api.username == existing_user.username
        assert user_api.email == existing_user.email
        assert user_api.role == existing_user.role

    def test_get_not_found(self, authorization_admin_header, users_data: list[User], client: TestClient):  # noqa: ARG002
        fake_non_existing_user_id = uuid.uuid4()
        response = client.get(f"/user/{fake_non_existing_user_id}", headers=authorization_admin_header)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGetUsersAPI:
    def test_get_users(self, authorization_admin_header: dict, client: TestClient, users_data: list[UserDTO]):
        response = client.post("/users/", headers=authorization_admin_header, json={})
        assert response.status_code == status.HTTP_200_OK

        def find_user_pagination(user: UserDTO):
            def wrapper(user_result: dict):
                user_result_api = UserResultAPI(**user_result)
                return (
                    str(user.id) == str(user_result_api.id)
                    and user.username == user_result_api.username
                    and user.email == user_result_api.email
                )

            return wrapper

        pagination = PaginationResultAPI(**response.json())
        for user in users_data:
            res = list(filter(find_user_pagination(user), pagination.items))
            assert len(list(res)) > 0

    @pytest.mark.parametrize(
        ("page", "page_items", "total_items", "filter_name", "filter_email", "filter_roles"),
        [
            (1, 1, 5, None, None, None),
            (1, 1, 0, "Dont_exist_name", None, None),
            (1, 1, 0, None, "Dont_exist_email", None),
            (1, 1, 0, None, "551fdb7b-b9bb-4d36-b5ad-853bd3a3fb49", None),
            (1, 1, 3, "Admin", None, None),
            (1, 1, 1, "admin", "admin1", None),
            (1, 1, 3, "Admin", None, [0, 1]),
            (1, 1, 2, None, None, [0]),
            (1, 1, 1, "admintodoapp", None, None),
            (1, 1, 0, "ratatatata", None, None),
        ],
    )
    def test_get_users_with_filters(
        self,
        page: int,
        page_items: int,
        total_items: int,
        filter_name: str | None,
        filter_email: str | None,
        filter_roles: list[int] | None,
        authorization_admin_header: dict,
        client: TestClient,
        users_data: list[UserDTO],  # noqa: ARG002
    ):
        body = {
            "page": page,
            "items": page_items,
            "filters": {
                "username": filter_name,
                "email": filter_email,
                "roles": filter_roles,
            },
        }

        response = client.post("/users/", headers=authorization_admin_header, json=body)
        assert response.status_code == status.HTTP_200_OK

        pagination = PaginationResultAPI(**response.json())
        assert len(pagination.items) <= page_items
        assert pagination.total_items == total_items
