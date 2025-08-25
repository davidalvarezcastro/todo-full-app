FROM python:3.12-alpine as builder

RUN pip install poetry==2.0.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
# poetry needs a README file
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

FROM python:3.12-alpine as base

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"


COPY --from=builder /app/.venv /app/.venv 

FROM base as local

VOLUME [ "/app/" ]

WORKDIR /app/todoapp

ENTRYPOINT ["python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "main:app","--reload" ,"--host", "0.0.0.0", "--port", "8000"]

