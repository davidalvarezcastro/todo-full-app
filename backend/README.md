# FastAPI Backend TodoAPP

![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-646464?logo=python&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-323232?logo=alembic&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?logo=jsonwebtokens&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

Todo API built with FastAPI and SQLAlchemy, featuring JWT authentication, Alembic migrations, and a clean architecture approach.

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – Web framework for APIs
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM for database models
- [Alembic](https://alembic.sqlalchemy.org/) – Database migrations
- [JWT](https://jwt.io/) – Authentication and authorization
- [Docker](https://www.docker.com/) – Containerization for development and production

### Architecture Patterns

- **Adapter / Domain pattern** – Clean separation between infrastructure and business logic
- **Command & Query pattern** – Clear distinction between write (commands) and read (queries) operations
- **DTO models: Database → Business Logic (Models) → API Views** – Well-defined data flow

---

## Authentication

- **JWT-based authentication** (access & refresh tokens)
- Protect routes with Depends(get_current_user) in FastAPI
- Tokens include user ID and role for authorization checks

```python
from fastapi import Depends
from todoapp.domain.models.user import UserInfo, UserRole
from todoapp.adapters.app.dependencies import get_todos_service
from todoapp.domain.services.todos.todos_service import TodosService
from todoapp.adapters.app.controllers.common.authorization import Authorization
from todoapp.adapters.app.controllers.common.conversion_api_domain import ConversionAPIDomain


class AddTodoAPI(ConversionAPIDomain):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    priority: int = Field(gt=0, lte=10)

@app.get("/todos")
def add_todo(
    add_todo_data: AddTodoAPI,
    todos_service: Annotated[TodosService, Depends(get_todos_service)],
    current_user: Annotated[UserInfo, Depends(Authorization([UserRole.ADMIN, UserRole.NORMAL]))],
) -> TodoResultAPI:
    add_todo_command: AddTodoCommand = add_todo_data.to_domain(AddTodoCommand)
    add_todo_command.owner_id = current_user.user_id
    return todos_service.add_todo(add_todo_command=add_todo_command)
```

---

## Project Setup

### 1. Clone the repository

```sh
$ git clone https://github.com/davidalvarezcastro/todo-full-app.git
$ cd todo-full-app/backend
```

### 2. Setup development enviroment

```bash
$ poetry install
```

### 3. Run app

Deploy dev services using docker-compose.yml.

### 4. Testing app

```bash
$ poetry run pytest tests
```
