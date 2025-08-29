from typing import Annotated

import attrs
from fastapi import APIRouter, Depends, status
from pydantic import Field

from todoapp.adapters.app.controllers.common.authorization import Authorization
from todoapp.adapters.app.controllers.common.base_controller import BaseController
from todoapp.adapters.app.controllers.common.conversion_api_domain import ConversionAPIDomain
from todoapp.adapters.app.controllers.todos.dependencies import get_authorized_todo_or_404
from todoapp.adapters.app.controllers.todos.todo_result_api import TodoResultAPI
from todoapp.adapters.app.dependencies import get_todos_service
from todoapp.domain.models.user import UserInfo, UserRole
from todoapp.domain.services.todos.commands.add_todo import AddTodoCommand
from todoapp.domain.services.todos.commands.delete_todo import DeleteTodoCommand
from todoapp.domain.services.todos.commands.edit_todo import EditTodoCommand
from todoapp.domain.services.todos.queries.get_todo import GetTodoQuery
from todoapp.domain.services.todos.todos_dtos import TodoDTO
from todoapp.domain.services.todos.todos_service import TodosService


class AddTodoAPI(ConversionAPIDomain):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    priority: int = Field(gt=0, lte=10)


class EditTodoAPI(ConversionAPIDomain):
    description: str = Field(min_length=3)
    priority: int = Field(gt=0, lte=10)
    completed: bool = Field()


@attrs.define
class TodoController(BaseController):
    def _add_url_rules(self, controller: APIRouter) -> None:
        @controller.post(
            "/",
            status_code=status.HTTP_201_CREATED,
        )
        def add_todo(
            add_todo_data: AddTodoAPI,
            todos_service: Annotated[TodosService, Depends(get_todos_service)],
            current_user: Annotated[UserInfo, Depends(Authorization([UserRole.ADMIN, UserRole.NORMAL]))],
        ) -> TodoResultAPI:
            add_todo_command: AddTodoCommand = add_todo_data.to_domain(AddTodoCommand)
            add_todo_command.owner_id = current_user.user_id
            return todos_service.add_todo(add_todo_command=add_todo_command)

        @controller.put(
            "/{todo_id}",
            status_code=status.HTTP_200_OK,
        )
        def edit_todo(
            edit_todo_data: EditTodoAPI,
            todo: Annotated[TodoDTO, Depends(get_authorized_todo_or_404)],
            todos_service: Annotated[TodosService, Depends(get_todos_service)],
        ) -> TodoResultAPI:
            edit_todo_command: EditTodoCommand = edit_todo_data.to_domain(EditTodoCommand)
            edit_todo_command.id = todo.id
            return todos_service.edit_todo(edit_todo_command=edit_todo_command)

        @controller.delete(
            "/{todo_id}",
            status_code=status.HTTP_204_NO_CONTENT,
        )
        def delete_todo(
            todo: Annotated[TodoDTO, Depends(get_authorized_todo_or_404)],
            todos_service: Annotated[TodosService, Depends(get_todos_service)],
        ):
            todos_service.delete_todo(delete_todo_command=DeleteTodoCommand(id=todo.id))

        @controller.get(
            "/{todo_id}",
            status_code=status.HTTP_200_OK,
        )
        def get_todo(
            todo: Annotated[TodoDTO, Depends(get_authorized_todo_or_404)],
        ) -> TodoResultAPI:
            return TodoResultAPI.from_domain(todo)
