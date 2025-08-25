from todoapp.adapters.database.models import TodosORM
from todoapp.domain.models.todos import Todo

Todo.orm_cls = TodosORM
