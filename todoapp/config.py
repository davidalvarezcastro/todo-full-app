from __future__ import annotations

import os
from enum import StrEnum

import attrs


def _get_value_from_env_key(key: str):
    value = os.getenv(key, None)

    if value is None:
        raise ValueError(f"Enviroment key {key} is not defined!")

    return value


class Environments(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


@attrs.define
class Environment:
    environment: Environments = attrs.field(default=Environments.PRODUCTION)

    def is_testing(self) -> bool:
        return self.environment == Environments.TESTING

    def is_development(self) -> bool:
        return self.environment == Environments.DEVELOPMENT

    def is_production(self) -> bool:
        return self.environment == Environments.PRODUCTION


@attrs.define
class Config:
    environment: Environment | None = None

    db_engine: str | None = None
    db_host: str | None = None
    db_port: int | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_name: str | None = None

    admin_user_email: str | None = None
    admin_user_password: str | None = None

    jwt_secret: str | None = None
    jwt_token_expiration_seconds: int | None = None
    jwt_refresh_token_expiration_seconds: int | None = None

    def __attrs_post_init__(self):
        if self.environment is None:
            self.environment = Environment(Environments(_get_value_from_env_key("ENVIRONMENT")))

        self.db_engine = self.db_engine or _get_value_from_env_key("DB_ENGINE")
        self.db_host = self.db_host or _get_value_from_env_key("DB_HOST")
        self.db_port = self.db_port or int(_get_value_from_env_key("DB_PORT"))
        self.db_user = self.db_user or _get_value_from_env_key("DB_USER")
        self.db_password = self.db_password or _get_value_from_env_key("DB_PASSWORD")
        self.db_name = self.db_name or _get_value_from_env_key("DB_NAME")

        self.admin_user_email = self.admin_user_email or _get_value_from_env_key("ADMIN_USER_EMAIL")
        self.admin_user_password = self.admin_user_password or _get_value_from_env_key("ADMIN_USER_PASSWORD")

        self.jwt_secret = self.jwt_secret or _get_value_from_env_key("JWT_SECRET")
        self.jwt_token_expiration_seconds = self.jwt_token_expiration_seconds or int(
            _get_value_from_env_key("JWT_TOKEN_EXPIRATION_SECONDS")
        )
        self.jwt_refresh_token_expiration_seconds = self.jwt_refresh_token_expiration_seconds or int(
            _get_value_from_env_key("JWT_REFRESH_TOKEN_EXPIRATION_SECONDS")
        )
