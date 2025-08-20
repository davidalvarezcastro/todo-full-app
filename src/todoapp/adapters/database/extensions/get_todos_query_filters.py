from todoapp.domain.services.todos.queries.get_todos import GetTodosQueryFilters


def get_predicate(self: GetTodosQueryFilters):
    pass


GetTodosQueryFilters.get_predicate = get_predicate
