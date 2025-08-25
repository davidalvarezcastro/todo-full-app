import uuid
from typing import Annotated

import attrs
from fastapi import APIRouter, Depends, status
from pydantic import Field

from todoapp.adapters.app.controllers.common.base_controller import BaseController
from todoapp.adapters.app.controllers.common.conversion_api_domain import ConversionAPIDomain
from todoapp.adapters.app.controllers.todos.todo_result_api import TodoResultAPI
from todoapp.adapters.app.dependencies import get_todos_service
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
    # owner_id # TODO: cuando esté la relación de usuarios


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
        ) -> TodoResultAPI:
            return todos_service.add_todo(add_todo_command=add_todo_data.to_domain(AddTodoCommand))

        @controller.put(
            "/{todo_id}",
            status_code=status.HTTP_200_OK,
        )
        def edit_todo(
            todo_id: uuid.UUID,
            edit_todo_data: EditTodoAPI,
            todos_service: Annotated[TodosService, Depends(get_todos_service)],
        ) -> TodoResultAPI:
            edit_todo_command: EditTodoCommand = edit_todo_data.to_domain(EditTodoCommand)
            edit_todo_command.id = todo_id

            return todos_service.edit_todo(edit_todo_command=edit_todo_command)

        @controller.delete(
            "/{todo_id}",
            status_code=status.HTTP_204_NO_CONTENT,
        )
        def delete_todo(
            todo_id: uuid.UUID,
            todos_service: Annotated[TodosService, Depends(get_todos_service)],
        ):
            todos_service.delete_todo(delete_todo_command=DeleteTodoCommand(id=todo_id))

        @controller.get(
            "/{todo_id}",
            status_code=status.HTTP_200_OK,
        )
        def get_todo(
            todo_id: uuid.UUID,
            todos_service: Annotated[TodosService, Depends(get_todos_service)],
        ) -> TodoResultAPI:
            todo: TodoDTO = todos_service.get_todo(get_todo_query=GetTodoQuery(id=todo_id))
            return TodoResultAPI.from_domain(todo)
