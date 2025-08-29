import uuid

import pytest

from todoapp.domain.models.user import UserInfo, UserRole


def check_user_data(user_dict: dict, user_info: UserInfo):
    assert user_dict["user_id"] == user_info.user_id
    assert user_dict["email"] == user_info.email
    assert user_dict["roles"] == [role.value for role in user_info.roles]


def test_to_dict_serializes_correctly(user_custom_data):
    user_id = str(uuid.uuid4())
    user_info = user_custom_data(custom_uuid=user_id)

    result = user_info.to_dict()

    check_user_data(user_dict=result, user_info=user_info)


def test_from_dict_deserializes_correctly():
    user_id = str(uuid.uuid4())
    data = {
        "user_id": user_id,
        "email": "test@example.com",
        "roles": [UserRole.ADMIN.value],
    }

    user_info = UserInfo.from_dict(data)

    check_user_data(user_dict=data, user_info=user_info)


def test_is_admin_true(user_custom_data):
    user_info = user_custom_data(role=UserRole.ADMIN)

    assert user_info.is_admin() is True


def test_is_admin_false(user_custom_data):
    user_info = user_custom_data(role=UserRole.NORMAL)

    assert user_info.is_admin() is False


def test_from_dict_with_invalid_uuid_raises():
    data = {
        "user_id": "not-a-uuid",
        "email": "invalid@example.com",
        "roles": [UserRole.NORMAL.value],
    }

    with pytest.raises(ValueError):
        UserInfo.from_dict(data)
