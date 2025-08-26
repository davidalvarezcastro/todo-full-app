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
        return self == Environments.TESTING

    def is_development(self) -> bool:
        return self == Environments.DEVELOPMENT

    def is_production(self) -> bool:
        return self == Environments.PRODUCTION


@attrs.define
class Config:
    environment: Environment = attrs.field(
        default=Environment(Environments(_get_value_from_env_key(key="ENVIRONMENT")))
    )

    db_engine: str = attrs.field(default=_get_value_from_env_key(key="DB_ENGINE"))
    db_host: str = attrs.field(default=_get_value_from_env_key(key="DB_HOST"))
    db_port: int = attrs.field(default=_get_value_from_env_key(key="DB_PORT"))
    db_user: str = attrs.field(default=_get_value_from_env_key(key="DB_USER"))
    db_password: str = attrs.field(default=_get_value_from_env_key(key="DB_PASSWORD"))
    db_name: str = attrs.field(default=_get_value_from_env_key(key="DB_NAME"))

    admin_user_email: str = attrs.field(default=_get_value_from_env_key(key="ADMIN_USER_EMAIL"))
    admin_user_password: str = attrs.field(default=_get_value_from_env_key(key="ADMIN_USER_PASSWORD"))

    jwt_secret: str = attrs.field(default=_get_value_from_env_key(key="JWT_SECRET"))
    jwt_token_expiration_seconds: int = attrs.field(
        default=int(_get_value_from_env_key(key="JWT_TOKEN_EXPIRATION_SECONDS"))
    )
    jwt_refresh_token_expiration_seconds: int = attrs.field(
        default=int(_get_value_from_env_key(key="JWT_REFRESH_TOKEN_EXPIRATION_SECONDS"))
    )
