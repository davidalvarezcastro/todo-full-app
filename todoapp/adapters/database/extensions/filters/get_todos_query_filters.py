from sqlalchemy import and_

from todoapp.adapters.database.models import TodosORM
from todoapp.domain.services.todos.queries.get_todos import GetTodosQueryFilters


def get_predicate(self: GetTodosQueryFilters):
    filter_conditions = []

    if self.priority is not None:
        filter_conditions.append(TodosORM.priority == self.priority)

    return and_(*filter_conditions) if len(filter_conditions) > 0 else None


GetTodosQueryFilters.get_predicate = get_predicate
