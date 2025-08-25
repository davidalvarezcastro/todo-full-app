from todoapp.adapters.database.models import TodosORM
from todoapp.domain.models.todo import Todo

Todo.orm_cls = TodosORM
