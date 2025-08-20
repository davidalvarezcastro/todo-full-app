from abc import ABC, abstractmethod

from fastapi import APIRouter, FastAPI


class BaseController(ABC):
    def register_on_app(self, app: "FastAPI", url_prefix: str = "", tags: list[str] | None = None):
        blueprint = APIRouter(prefix=url_prefix, tags=tags if tags else ["app"])
        self._add_url_rules(blueprint)
        app.include_router(blueprint)

    @abstractmethod
    def _add_url_rules(self, controller: "APIRouter") -> None:
        raise NotImplementedError
