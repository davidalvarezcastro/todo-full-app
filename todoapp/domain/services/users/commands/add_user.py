import uuid

import attrs

from todoapp.domain.exceptions import ConflictError
from todoapp.domain.models.user import User, UserRole
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.auth.auth import Auth
from todoapp.domain.services.common.command_handler_base import CommandBase, CommandHandlerBase
from todoapp.domain.services.users.users_dtos import UserDTO


@attrs.define
class AddUserCommand(CommandBase):
    username: str = attrs.field(validator=[attrs.validators.min_len(3)])
    email: str = attrs.field(validator=[attrs.validators.max_len(320), attrs.validators.matches_re(r"^\S+@\S+\.\S+$")])
    password: str = attrs.field(validator=[attrs.validators.min_len(6)])
    role: UserRole = attrs.field(validator=[attrs.validators.instance_of(UserRole)])


@attrs.define
class AddUserCommandHandler(CommandHandlerBase):
    data_context: DataContext

    def handle(self, command: AddUserCommand) -> UserDTO:
        user = self.data_context.users_repo.get_by_email(command.email)
        if user:
            raise ConflictError(f"User with email '{command.email}' already exists")

        password = Auth.create_hashed_password(command.password)

        user = User(
            id=str(uuid.uuid4()),
            username=command.username,
            email=command.email,
            password=password,
            role=command.role,
            is_active=True,
        )

        user = self.data_context.users_repo.add(entity=user)

        return UserDTO.from_model(user)
