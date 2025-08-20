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
    db_url: str = attrs.field(default=_get_value_from_env_key(key="DB_URL"))
