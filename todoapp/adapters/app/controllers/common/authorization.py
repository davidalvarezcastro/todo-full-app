from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from todoapp.adapters.app.dependencies import get_token_handler
from todoapp.domain.models.user import UserInfo, UserRole
from todoapp.domain.services.auth.token import AbstractToken


class Authorization(HTTPBearer):
    def __init__(self, allowerd_roles: list[UserRole] | None = None):
        super().__init__()
        self.allowed_roles: list[UserRole] = allowerd_roles if allowerd_roles else list(UserRole)

    async def __call__(self, request: Request, token_handler: Annotated[AbstractToken, Depends(get_token_handler)]):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        return self._validate_token_and_roles(token_handler, credentials)

    def _validate_token_and_roles(
        self, token_handler: AbstractToken, credentials: HTTPAuthorizationCredentials
    ) -> UserInfo:
        if not credentials or credentials.scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme.")

        if not token_handler.is_valid_token(credentials.credentials):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")

        token_data = token_handler.get_token_data(credentials.credentials)
        if token_data.get("is_refresh_token"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")

        user_info = UserInfo.from_dict(token_data)

        if not any(role in self.allowed_roles for role in user_info.roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions.")

        return user_info
