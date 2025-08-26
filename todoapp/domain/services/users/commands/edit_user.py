import logging
import uuid

import attrs

from todoapp.domain.exceptions import NotFoundError
from todoapp.domain.models.user import User, UserRole
from todoapp.domain.repositories.data_context import DataContext
from todoapp.domain.services.auth.auth import Auth
from todoapp.domain.services.common.command_handler_base import CommandBase, CommandHandlerBase
from todoapp.domain.services.users.users_dtos import UserDTO
from todoapp.regex import EMAIL_REGEX


@attrs.define
class EditUserCommand(CommandBase):
    id: uuid.UUID = attrs.field(init=False)
    email: str | None = attrs.field(
        validator=[
            attrs.validators.optional(attrs.validators.max_len(320)),
            attrs.validators.optional(attrs.validators.matches_re(EMAIL_REGEX)),
        ],
        default=None,
    )
    password: str | None = attrs.field(validator=[attrs.validators.optional(attrs.validators.min_len(6))], default=None)
    role: UserRole | None = attrs.field(
        validator=[attrs.validators.optional(attrs.validators.instance_of(UserRole))], default=None
    )
    active: bool | None = attrs.field(default=True)


@attrs.define
class EditUserCommandHandler(CommandHandlerBase):
    data_context: DataContext

    def handle(self, command: EditUserCommand) -> UserDTO:
        user: User = self.data_context.users_repo.get_by_id(str(command.id))
        if not user:
            raise NotFoundError(f"User with email '{command.email}' does not exists")

        logging.error("\n\n\n\n\n editusercommand \n\n\n\n\n")

        if command.password:
            (password, salt) = Auth.create_hashed_password_salt(command.password)
            user.password = password
            user.salt = salt

        if command.email:
            user.email = command.email
        if command.role:
            user.role = command.role
        if command.active is not None:
            user.is_active = command.active

        user = self.data_context.users_repo.update(entity=user)
        return UserDTO.from_model(user)
