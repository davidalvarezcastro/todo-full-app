from datetime import timedelta

import attrs
from passlib.context import CryptContext

from todoapp.config import Config
from todoapp.domain.commons.date_utils import get_utc_now
from todoapp.domain.exceptions import UnauthorizedError
from todoapp.domain.models.user import User, UserInfo
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.auth.auth_dtos import AuthTokenResultDTO, LoginDTO
from todoapp.domain.services.auth.token import AbstractToken

# Configuración de Passlib
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


@attrs.define
class Auth:
    data_context: DataContext
    config: Config
    token_handler: AbstractToken

    def login(self, login_data: LoginDTO) -> AuthTokenResultDTO:
        user: User = self.data_context.users_repo.get_by_email(email=login_data.email)
        if user is None:
            raise UnauthorizedError("Invalid credentials. Please check your username and password.")

        if not Auth.check_password(plain_password=login_data.password, hashed_password=user.password):
            raise UnauthorizedError("Invalid credentials. Please check your username and password.")

        user_info = UserInfo(user_id=user.id, email=user.email, roles=[user.role])
        return self._get_login_result(user_info)

    def refresh(self, token: str):
        if not self.token_handler.is_valid_token(token):
            raise UnauthorizedError("Invalid refresh token.")

        user_info = UserInfo.from_dict(self.token_handler.get_token_data(token))
        return self._get_login_result(user_info)

    def _get_login_result(self, user_info: UserInfo) -> AuthTokenResultDTO:
        token_expiration_date = get_utc_now() + timedelta(seconds=self.config.jwt_token_expiration_seconds)
        refresh_token_expiration_date = get_utc_now() + timedelta(
            seconds=self.config.jwt_refresh_token_expiration_seconds
        )

        return AuthTokenResultDTO(
            token=self.token_handler.create_token(token_expiration_date, user_info.to_dict()),
            token_expiration_date=token_expiration_date,
            refresh_token=self.token_handler.create_token(
                refresh_token_expiration_date, {"is_refresh_token": True, **user_info.to_dict()}
            ),
            refresh_token_expiration_date=refresh_token_expiration_date,
        )

    @classmethod
    def create_hashed_password(cls, password: str) -> tuple[str, str]:
        hashed_password = pwd_context.hash(password)
        return hashed_password

    @classmethod
    def check_password(cls, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
