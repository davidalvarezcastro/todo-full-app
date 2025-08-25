from typing import Annotated

from fastapi.params import Depends

from todoapp.adapters.database.database import DatabaseConnector
from todoapp.config import Config
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.todos.todos_service import TodosService


def get_config() -> Config:
    return Config()


def get_database_connector(config: Annotated[Config, Depends(get_config)]) -> DatabaseConnector:
    db_url = f"{config.db_engine}:///{config.db_url}"

    database_conector = DatabaseConnector(db_url=db_url)
    return database_conector


def get_data_context(database_connector: Annotated[DatabaseConnector, Depends(get_database_connector)]) -> DataContext:
    return DataContext(database_connector=database_connector)


def get_todos_service(
    data_context: Annotated[DataContext, Depends(get_data_context)],
) -> TodosService:
    return TodosService(data_context=data_context)
