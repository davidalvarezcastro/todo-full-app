import uuid

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from todoapp.adapters.app.controllers.common.pagination_api import PaginationResultAPI
from todoapp.adapters.app.controllers.todos.todo_result_api import TodoResultAPI
from todoapp.domain.models.todo import Todo
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.todos.todos_dtos import TodoDTO


class TestAddTodoAPI:
    def test_creates_todo_when_valid_data(
        self, authorization_admin_header, datacontext: DataContext, client: TestClient
    ):
        todo_request_body = {"title": "faketitle", "description": "fake description", "priority": 5}
        response = client.post("/todo/", headers=authorization_admin_header, json=todo_request_body)
        assert response.status_code == status.HTTP_201_CREATED

        todo_result = TodoResultAPI(**response.json())
        assert todo_result.title == todo_request_body["title"]
        assert todo_result.description == todo_request_body["description"]
        assert todo_result.priority == todo_request_body["priority"]

        todo: Todo = datacontext.todos_repo.get_by_id(id=str(todo_result.id))
        assert todo
        assert todo.title == todo_request_body["title"]
        assert todo.description == todo_request_body["description"]
        assert todo.priority == todo_request_body["priority"]

    def test_add_exiting(self, authorization_admin_header, todos_data: list[Todo], client: TestClient):
        existing_todo = todos_data[0]
        todo_request_body = {
            "title": existing_todo.title,
            "description": existing_todo.description,
            "priority": 5,
        }
        response = client.post("/todo/", headers=authorization_admin_header, json=todo_request_body)
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.parametrize(
        "title, description, priority",
        [
            ("fake title", "fake description", 0),
            ("fake title", "fake description", -1),
            ("fa", "fakxcvxcxcv@czxczx", 5),
        ],
    )
    def test_add_validation_error(
        self, title: str, description: str, priority: int, authorization_admin_header, client: TestClient
    ):
        todo_request_body = {"title": title, "description": description, "priority": priority}
        response = client.post("/todo/", headers=authorization_admin_header, json=todo_request_body)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestEditTodoAPI:
    @pytest.mark.parametrize(
        "description, priority, completed",
        [("new description", 2, False), ("fake description", 1, True)],
    )
    def test_edit_success(
        self,
        description: str,
        priority: int,
        completed: bool,
        authorization_admin_header,
        datacontext: DataContext,
        todos_data: list[Todo],
        client: TestClient,
    ):
        existing_todo = todos_data[1]
        todo_request_body = {
            "description": description,
            "priority": priority,
            "completed": completed,
        }
        response = client.put(f"/todo/{existing_todo.id}", headers=authorization_admin_header, json=todo_request_body)
        assert response.status_code == status.HTTP_200_OK

        todo_result = TodoResultAPI(**response.json())
        assert str(todo_result.id) == existing_todo.id
        assert todo_result.description == todo_request_body["description"]
        assert todo_result.priority == todo_request_body["priority"]
        assert todo_result.completed == todo_request_body["completed"]

        todo: Todo = datacontext.todos_repo.get_by_id(id=str(todo_result.id))
        assert todo
        assert todo.description == todo_request_body["description"]
        assert todo.priority == todo_request_body["priority"]
        assert todo.completed == todo_request_body["completed"]

    @pytest.mark.parametrize(
        "description, priority, completed",
        [
            ("fa", -10, True),
            ("fake description", 8, None),
            ("fake description", 8, "jasdkds"),
        ],
    )
    def test_edit_validation_error(
        self,
        description: str,
        priority: int,
        completed: bool,
        authorization_admin_header,
        todos_data: list[Todo],
        client: TestClient,
    ):
        existing_todo = todos_data[1]
        todo_request_body = {
            "description": description,
            "priority": priority,
            "completed": completed,
        }
        response = client.put(f"/todo/{existing_todo.id}", headers=authorization_admin_header, json=todo_request_body)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestDeleteTodoAPI:
    def test_delete_success(
        self, authorization_admin_header, todos_data: list[Todo], datacontext: DataContext, client: TestClient
    ):
        existing_todo = todos_data[0]
        response = client.delete(f"/todo/{existing_todo.id}", headers=authorization_admin_header)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        todo: Todo = datacontext.todos_repo.get_by_id(id=str(existing_todo.id))
        assert todo is None


class TestGetTodoAPI:
    def test_get_success(self, authorization_admin_header, todos_data: list[Todo], client: TestClient):
        existing_todo = todos_data[0]
        response = client.get(f"/todo/{existing_todo.id}", headers=authorization_admin_header)
        assert response.status_code == status.HTTP_200_OK

        todo_api: TodoResultAPI = TodoResultAPI(**response.json())
        assert str(todo_api.id) == existing_todo.id
        assert todo_api.title == existing_todo.title
        assert todo_api.description == existing_todo.description
        assert todo_api.priority == existing_todo.priority
        assert todo_api.completed == existing_todo.completed

    def test_get_not_found(self, authorization_admin_header, todos_data: list[Todo], client: TestClient):  # noqa: ARG002
        fake_non_existing_todo_id = uuid.uuid4()
        response = client.get(f"/todo/{fake_non_existing_todo_id}", headers=authorization_admin_header)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGetTodosAPI:
    def test_get_todos(self, authorization_admin_header: dict, client: TestClient, todos_data: list[Todo]):
        response = client.post("/todos/", headers=authorization_admin_header, json={})
        assert response.status_code == status.HTTP_200_OK

        def find_todo_pagination(todo: TodoDTO):
            def wrapper(todo_result: dict):
                todo_result_api = TodoResultAPI(**todo_result)
                return (
                    str(todo.id) == str(todo_result_api.id)
                    and todo.title == todo_result_api.title
                    and todo.description == todo_result_api.description
                )

            return wrapper

        pagination = PaginationResultAPI(**response.json())
        for todo in todos_data:
            res = list(filter(find_todo_pagination(todo), pagination.items))
            assert len(list(res)) > 0

    @pytest.mark.parametrize(
        ("page", "page_items", "total_items", "filter_priority", "filter_owner_id"),
        [
            (1, 1, 2, 5, None),
            (1, 1, 0, 8, None),
            (1, 1, 2, None, "d2a09b40-9da4-4db7-8035-cd9a50a192fd"),
            (1, 1, 0, 2, "b506879f-e5ed-49d0-8960-338fd266525e"),
            (1, 1, 2, 6, "b506879f-e5ed-49d0-8960-338fd266525e"),
        ],
    )
    def test_get_todos_with_filters(
        self,
        page: int,
        page_items: int,
        total_items: int,
        filter_priority: int | None,
        filter_owner_id: str | None,
        authorization_admin_header: dict,
        client: TestClient,
        todos_data: list[Todo],  # noqa: ARG002
    ):
        body = {
            "page": page,
            "items": page_items,
            "filters": {
                "priority": filter_priority,
                "owner_id": filter_owner_id,
            },
        }

        response = client.post("/todos/", headers=authorization_admin_header, json=body)
        assert response.status_code == status.HTTP_200_OK

        pagination = PaginationResultAPI(**response.json())
        assert len(pagination.items) <= page_items
        assert pagination.total_items == total_items
