from todoapp.adapters.database.models import TodosORM, UsersORM
from todoapp.domain.models.todo import Todo
from todoapp.domain.models.user import User

Todo.orm_cls = TodosORM
User.orm_cls = UsersORM
