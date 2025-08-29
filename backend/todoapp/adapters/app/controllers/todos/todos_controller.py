from typing import Annotated

import attrs
from fastapi import APIRouter, Depends, status

from todoapp.adapters.app.controllers.common.authorization import Authorization
from todoapp.adapters.app.controllers.common.base_controller import BaseController
from todoapp.adapters.app.controllers.common.conversion_api_domain import ConversionAPIDomain
from todoapp.adapters.app.controllers.common.pagination_api import PaginationFiltersAPI, PaginationResultAPI
from todoapp.adapters.app.controllers.todos.todo_result_api import TodoResultAPI
from todoapp.adapters.app.dependencies import get_todos_service
from todoapp.domain.models.user import UserInfo, UserRole
from todoapp.domain.services.todos.queries.get_todos import GetTodosQuery, GetTodosQueryFilters
from todoapp.domain.services.todos.todos_service import TodosService


class GetTodosFiltersAPI(ConversionAPIDomain):
    priority: int | None = None
    owner_id: str | None = None  # Admin user can filter by owner


@attrs.define
class TodosController(BaseController):
    def _add_url_rules(self, controller: APIRouter) -> None:
        @controller.post(
            "/",
            status_code=status.HTTP_200_OK,
        )
        def get_todos(
            body: PaginationFiltersAPI[GetTodosFiltersAPI],
            todos_service: Annotated[TodosService, Depends(get_todos_service)],
            current_user: Annotated[UserInfo, Depends(Authorization([UserRole.ADMIN, UserRole.NORMAL]))],
        ) -> PaginationResultAPI[TodoResultAPI]:
            get_todos_query: GetTodosQuery = body.to_domain(GetTodosQuery)

            if get_todos_query.filters is None:
                get_todos_query.filters = GetTodosQueryFilters()

            if not current_user.is_admin():
                get_todos_query.filters.owner_id = current_user.user_id

            todos = todos_service.get_todos(get_todos_query=get_todos_query)
            return PaginationResultAPI.from_domain(todos)
