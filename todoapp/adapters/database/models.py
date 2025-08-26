from sqlalchemy import VARCHAR, Boolean, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from todoapp.domain.models.user import UserRole


class BaseORM(DeclarativeBase):
    pass


class UsersORM(BaseORM):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    salt: Mapped[str] = mapped_column(VARCHAR(255))
    role: Mapped[int] = mapped_column(Integer, default=UserRole.NORMAL.value)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class TodosORM(BaseORM):
    __tablename__ = "todos"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    priority: Mapped[int] = mapped_column(Integer)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    # owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner_id: Mapped[int] = mapped_column(Integer)
