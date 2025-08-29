from fastapi import Request, status
from fastapi.responses import JSONResponse

from todoapp.adapters.app.middlewares.base_middleware import BaseMiddleware
from todoapp.domain.exceptions import ConflictError, NotFoundError, UnauthorizedError


class ExceptionsMiddleware(BaseMiddleware):
    async def middleware_process(self, request: Request, call_next):
        try:
            return await call_next(request)
        except NotFoundError as e:
            status_code = status.HTTP_404_NOT_FOUND
            message = e.message
        except ConflictError as e:
            status_code = status.HTTP_409_CONFLICT
            message = e.message
        except UnauthorizedError as e:
            status_code = status.HTTP_401_UNAUTHORIZED
            message = e.message

        return JSONResponse(status_code=status_code, content={"details": {"msg": message}})
