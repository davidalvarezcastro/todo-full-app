import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status

from todoapp.adapters.app.controllers.common.authorization import Authorization
from todoapp.adapters.app.dependencies import get_todos_service
from todoapp.domain.models.user import UserInfo, UserRole
from todoapp.domain.services.todos.queries.get_todo import GetTodoQuery
from todoapp.domain.services.todos.todos_dtos import TodoDTO
from todoapp.domain.services.todos.todos_service import TodosService


def get_authorized_todo_or_404(
    todo_id: uuid.UUID,
    todos_service: Annotated[TodosService, Depends(get_todos_service)],
    current_user: Annotated[UserInfo, Depends(Authorization([UserRole.ADMIN, UserRole.NORMAL]))],
) -> TodoDTO:
    todo: TodoDTO = todos_service.get_todo(GetTodoQuery(id=todo_id))

    if not current_user.is_admin() and todo.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")

    return todo
