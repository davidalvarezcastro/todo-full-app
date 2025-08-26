from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from todoapp.adapters.app.controllers.barfoo.barfoo_controller import BarFooController
from todoapp.adapters.app.controllers.todos.todo_controller import TodoController
from todoapp.adapters.app.controllers.todos.todos_controller import TodosController
from todoapp.adapters.app.dependencies import get_database_connector
from todoapp.adapters.app.middlewares.exceptions_middleware import ExceptionsMiddleware
from todoapp.adapters.database.seed import Seed
from todoapp.config import Config


def create_app() -> FastAPI:
    config = Config()

    database_connector = get_database_connector(config=config)
    database_connector.migrate()

    if not config.environment.is_testing():
        Seed(config).seed()

    app = FastAPI(root_path="/api/v1", title="Todos Repo API", version="0.0.1")

    BarFooController().register_on_app(app=app, url_prefix="", tags=["Healthcheck"])

    TodoController().register_on_app(app=app, url_prefix="/todo", tags=["Todos"])
    TodosController().register_on_app(app=app, url_prefix="/todos", tags=["Todos"])

    ExceptionsMiddleware().register_on_app(app=app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
