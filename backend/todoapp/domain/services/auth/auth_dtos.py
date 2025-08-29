from datetime import datetime

import attrs

from todoapp.regex import EMAIL_REGEX


@attrs.define
class AuthTokenResultDTO:
    token: str
    token_expiration_date: datetime
    refresh_token: str
    refresh_token_expiration_date: datetime


@attrs.define
class LoginDTO:
    email: str = attrs.field(
        validator=[attrs.validators.max_len(320), attrs.validators.matches_re(EMAIL_REGEX)],
    )
    password: str
