from typing import Annotated

from fastapi.params import Depends

from todoapp.adapters.database.database import DatabaseConnector
from todoapp.config import Config
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.auth.auth import Auth
from todoapp.domain.services.auth.token import AbstractToken, JWTToken
from todoapp.domain.services.todos.todos_service import TodosService
from todoapp.domain.services.users.users_service import UsersService


def get_config() -> Config:
    return Config()


def get_database_connector(config: Annotated[Config, Depends(get_config)]) -> DatabaseConnector:
    db_host = config.db_host if config.environment.is_testing() else "database"
    db_url = f"{config.db_engine}://{config.db_user}:{config.db_password}@{db_host}:{config.db_port}/{config.db_name}"

    database_conector = DatabaseConnector(db_url=db_url)
    return database_conector


def get_data_context(database_connector: Annotated[DatabaseConnector, Depends(get_database_connector)]) -> DataContext:
    return DataContext(database_connector=database_connector)


def get_token_handler(config: Annotated[Config, Depends(get_config)]) -> AbstractToken:
    return JWTToken(config.jwt_secret)


def get_todos_service(
    data_context: Annotated[DataContext, Depends(get_data_context)],
) -> TodosService:
    return TodosService(data_context=data_context)


def get_users_service(
    data_context: Annotated[DataContext, Depends(get_data_context)],
) -> UsersService:
    return UsersService(data_context)


def get_auth(
    data_context: Annotated[DataContext, Depends(get_data_context)],
    config: Annotated[Config, Depends(get_config)],
    token_handler: Annotated[AbstractToken, Depends(get_token_handler)],
) -> Auth:
    return Auth(data_context=data_context, config=config, token_handler=token_handler)
