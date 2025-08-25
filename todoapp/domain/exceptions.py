import attrs


@attrs.define
class MessageError(Exception):
    message: str


class NotFoundError(MessageError):
    pass


class ConflictError(MessageError):
    pass
