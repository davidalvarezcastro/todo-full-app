import re
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import Field

from todoapp.adapters.app.controllers.common.base_controller import BaseController
from todoapp.adapters.app.controllers.common.conversion_api_domain import ConversionAPIDomain
from todoapp.adapters.app.dependencies import get_auth, get_config
from todoapp.config import Config
from todoapp.domain.commons.date_utils import get_utc_now
from todoapp.domain.services.auth.auth import Auth
from todoapp.domain.services.auth.auth_dtos import LoginDTO
from todoapp.regex import EMAIL_REGEX


class LoginAPI(ConversionAPIDomain):
    email: str = Field(pattern=EMAIL_REGEX, max_length=320, examples=["bar@foo.com"])
    password: str


class AuthTokenResultAPI(ConversionAPIDomain):
    token: str
    token_expiration_date: datetime


REFRESH_TOKEN_HTTPONLY_COOKIE = "refresh_token"


class AuthController(BaseController):
    def _add_url_rules(self, controller: APIRouter) -> None:
        @controller.post("/oauth_login", status_code=200)
        def oauth_login(
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth: Annotated[Auth, Depends(get_auth)]
        ) -> AuthTokenResultAPI:
            """
            Login vía OAuth2.

            - **username**: Debe ser un email válido (ejemplo: `bar@foo.com`)
            - **password**: Tu contraseña
            """
            if not re.fullmatch(EMAIL_REGEX, form_data.username):
                raise HTTPException(status_code=400, detail="Username must be a valid email")

            login_result = auth.login(LoginDTO(email=form_data.username, password=form_data.password))
            return AuthTokenResultAPI.from_domain(login_result)

        @controller.post("/login", status_code=200)
        def login(
            login_data: LoginAPI,
            response: Response,
            config: Annotated[Config, Depends(get_config)],
            auth: Annotated[Auth, Depends(get_auth)],
        ) -> AuthTokenResultAPI:
            login_result = auth.login(login_data.to_domain(LoginDTO))

            response.set_cookie(
                key=REFRESH_TOKEN_HTTPONLY_COOKIE,
                value=login_result.refresh_token,
                httponly=True,
                secure=True if not config.environment.is_testing() else False,
                samesite="strict",
                max_age=int((login_result.refresh_token_expiration_date - get_utc_now()).total_seconds()),
            )

            return AuthTokenResultAPI.from_domain(login_result)

        @controller.post("/refresh", status_code=200)
        def refresh(
            request: Request,
            response: Response,
            config: Annotated[Config, Depends(get_config)],
            auth: Annotated[Auth, Depends(get_auth)],
        ) -> AuthTokenResultAPI:
            refresh_token = request.cookies.get("refresh_token")
            if not refresh_token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

            login_result = auth.refresh(refresh_token)

            response.set_cookie(
                key=REFRESH_TOKEN_HTTPONLY_COOKIE,
                value=login_result.refresh_token,
                httponly=True,
                secure=True if not config.environment.is_testing() else False,
                samesite="strict",
                max_age=int((login_result.refresh_token_expiration_date - get_utc_now()).total_seconds()),
            )

            return AuthTokenResultAPI.from_domain(login_result)
