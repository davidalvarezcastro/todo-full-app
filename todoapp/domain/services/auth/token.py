import abc
from datetime import datetime

import attrs
from jose import jwt


class AbstractToken(abc.ABC):
    @abc.abstractmethod
    def create_token(self, expiration_date: datetime, data: dict) -> str:
        pass

    @abc.abstractmethod
    def is_valid_token(self, token: str) -> bool:
        pass

    @abc.abstractmethod
    def get_token_data(self, token: str) -> dict:
        pass


@attrs.define
class JWTToken(AbstractToken):
    secret: str
    ending_algorithm: str = "HS256"

    def create_token(self, expiration_date: datetime, data: dict) -> str:
        jwt_data = {"exp": expiration_date, **data}

        return jwt.encode(
            jwt_data,
            self.secret,
            algorithm=self.ending_algorithm,
        )

    def is_valid_token(self, token: str) -> bool:
        try:
            jwt.decode(token, self.secret, algorithms=[self.ending_algorithm])
            return True
        except Exception:
            return False

    def get_token_data(self, token: str) -> dict:
        return jwt.decode(token, self.secret, algorithms=[self.ending_algorithm])
