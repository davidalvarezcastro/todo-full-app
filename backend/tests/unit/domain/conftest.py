import uuid

import pytest

from todoapp.domain.models.user import UserInfo, UserRole


@pytest.fixture
def user_custom_data():
    def _make_user(
        custom_uuid: str | None = None, role: UserRole = UserRole.NORMAL, email: str = "davalv@televes.com"
    ) -> UserInfo:
        return UserInfo(
            email=email,
            user_id=str(custom_uuid or uuid.uuid4()),
            roles=[role],
        )

    return _make_user


@pytest.fixture
def user_data(user_custom_data) -> UserInfo:
    return user_custom_data(custom_uuid="davalv", role=UserRole.NORMAL)
