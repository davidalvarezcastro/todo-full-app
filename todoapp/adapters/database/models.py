from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from todoapp.domain.models.user import UserRole


class BaseORM(DeclarativeBase):
    pass


class UsersORM(BaseORM):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    salt: Mapped[str] = mapped_column(String(255))
    role: Mapped[int] = mapped_column(Integer, default=UserRole.NORMAL.value)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class TodosORM(BaseORM):
    __tablename__ = "todos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1024))
    priority: Mapped[int] = mapped_column(Integer)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
