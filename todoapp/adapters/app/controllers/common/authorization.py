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

        self._check_credentials(token_handler, credentials)
        self._check_roles(token_handler, credentials.credentials)

    def _check_credentials(self, token_handler: AbstractToken, credentials: HTTPAuthorizationCredentials):
        if not credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization code.")

        if not credentials.scheme == "Bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme.")

        if not token_handler.is_valid_token(credentials.credentials):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired token.")

        if "is_refresh_token" in token_handler.get_token_data(credentials.credentials):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired token.")

    def _check_roles(self, token_handler: AbstractToken, token: str):
        user_info = UserInfo.from_dict(token_handler.get_token_data(token))

        for role in user_info.roles:
            if role in self.allowed_roles:
                return

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No permission to access this resource")
