from typing import Annotated

import attrs
from fastapi import APIRouter, Depends, status

from todoapp.adapters.app.controllers.common.authorization import Authorization
from todoapp.adapters.app.controllers.common.base_controller import BaseController
from todoapp.adapters.app.controllers.common.conversion_api_domain import ConversionAPIDomain
from todoapp.adapters.app.controllers.common.pagination_api import PaginationFiltersAPI, PaginationResultAPI
from todoapp.adapters.app.controllers.users.user_result_api import UserResultAPI
from todoapp.adapters.app.dependencies import get_users_service
from todoapp.domain.models.user import UserRole
from todoapp.domain.services.users.queries.get_users import GetUsersQuery
from todoapp.domain.services.users.users_service import UsersService


class GetUsersFiltersAPI(ConversionAPIDomain):
    username: str | None = None
    email: str | None = None
    roles: list[UserRole] | None = None


@attrs.define
class UsersController(BaseController):
    def _add_url_rules(self, controller: APIRouter) -> None:
        @controller.post(
            "/",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(Authorization([UserRole.ADMIN]))],
        )
        def get_users(
            body: PaginationFiltersAPI[GetUsersFiltersAPI],
            users_service: Annotated[UsersService, Depends(get_users_service)],
        ) -> PaginationResultAPI[UserResultAPI]:
            get_users_query = body.to_domain(GetUsersQuery)
            users = users_service.get_users(get_users_query=get_users_query)
            return PaginationResultAPI.from_domain(users)
