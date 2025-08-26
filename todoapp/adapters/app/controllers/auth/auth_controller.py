from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import Field

from todoapp.adapters.app.controllers.common.base_controller import BaseController
from todoapp.adapters.app.controllers.common.conversion_api_domain import ConversionAPIDomain
from todoapp.adapters.app.dependencies import get_auth
from todoapp.domain.services.auth.auth import Auth
from todoapp.domain.services.auth.auth_dtos import LoginDTO
from todoapp.regex import EMAIL_REGEX


class LoginAPI(ConversionAPIDomain):
    email: str = Field(pattern=EMAIL_REGEX, max_length=320, examples=["bar@foo.com"])
    password: str


class AuthTokenResultAPI(ConversionAPIDomain):
    token: str
    token_expiration_date: datetime
    refresh_token: str
    refresh_token_expiration_date: datetime


class AuthController(BaseController):
    def _add_url_rules(self, controller: APIRouter) -> None:
        @controller.post("/login", status_code=200)
        def login(login_data: LoginAPI, auth: Annotated[Auth, Depends(get_auth)]) -> AuthTokenResultAPI:
            login_result = auth.login(login_data.to_domain(LoginDTO))
            return AuthTokenResultAPI.from_domain(login_result)

        @controller.post("/refresh", status_code=200)
        def refresh(refresh_token: str, auth: Annotated[Auth, Depends(get_auth)]) -> AuthTokenResultAPI:
            login_result = auth.refresh(refresh_token)
            return AuthTokenResultAPI.from_domain(login_result)
