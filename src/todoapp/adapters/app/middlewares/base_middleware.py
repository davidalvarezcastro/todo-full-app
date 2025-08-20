import abc

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware


class BaseMiddleware(abc.ABC):
    def register_on_app(self, app: FastAPI):
        app.add_middleware(BaseHTTPMiddleware, self.middleware_process)

    @abc.abstractmethod
    async def middleware_process(self, request: Request, call_next):
        pass
