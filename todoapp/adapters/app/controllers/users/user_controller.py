import uuid
from typing import Annotated

import attrs
from fastapi import APIRouter, Depends, status
from pydantic import Field

from todoapp.adapters.app.controllers.common.base_controller import BaseController
from todoapp.adapters.app.controllers.common.conversion_api_domain import ConversionAPIDomain
from todoapp.adapters.app.controllers.users.user_result_api import UserResultAPI
from todoapp.adapters.app.dependencies import get_users_service
from todoapp.domain.models.user import UserRole
from todoapp.domain.services.users.commands.add_user import AddUserCommand
from todoapp.domain.services.users.commands.delete_user import DeleteUserCommand
from todoapp.domain.services.users.commands.edit_user import EditUserCommand
from todoapp.domain.services.users.queries.get_user import GetUserQuery
from todoapp.domain.services.users.users_dtos import UserDTO
from todoapp.domain.services.users.users_service import UsersService
from todoapp.regex import EMAIL_REGEX


class AddUserAPI(ConversionAPIDomain):
    username: str = Field(min_length=3)
    email: str = Field(pattern=EMAIL_REGEX, max_length=320, examples=["bar@foo.com"])
    password: str = Field(min_length=6)
    role: UserRole


class EditUserAPI(ConversionAPIDomain):
    email: str | None = Field(pattern=EMAIL_REGEX, max_length=320, examples=["bar@foo.com"], default=None)
    password: str | None = Field(min_length=6, default=None)
    role: UserRole | None = Field(default=None)
    active: bool | None = Field(default=True)


@attrs.define
class UserController(BaseController):
    def _add_url_rules(self, controller: APIRouter) -> None:
        @controller.post("/", status_code=status.HTTP_201_CREATED)
        def add_user(
            add_user_data: AddUserAPI, users_service: Annotated[UsersService, Depends(get_users_service)]
        ) -> UserResultAPI:
            return users_service.add_user(add_user_command=add_user_data.to_domain(AddUserCommand))

        @controller.put("/{user_id}", status_code=status.HTTP_200_OK)
        def edit_user(
            user_id: uuid.UUID,
            edit_user_data: EditUserAPI,
            users_service: Annotated[UsersService, Depends(get_users_service)],
        ) -> UserResultAPI:
            edit_user_command: EditUserCommand = edit_user_data.to_domain(EditUserCommand)
            edit_user_command.id = user_id

            return users_service.edit_user(edit_user_command=edit_user_command)

        @controller.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
        def delete_user(
            user_id: uuid.UUID,
            users_service: Annotated[UsersService, Depends(get_users_service)],
        ):
            users_service.delete_user(delete_user_command=DeleteUserCommand(id=user_id))

        @controller.get("/{user_id}", status_code=status.HTTP_200_OK)
        def get_user(
            user_id: uuid.UUID,
            users_service: Annotated[UsersService, Depends(get_users_service)],
        ) -> UserResultAPI:
            user: UserDTO = users_service.get_user(get_user_query=GetUserQuery(id=user_id))
            return UserResultAPI.from_domain(user)
