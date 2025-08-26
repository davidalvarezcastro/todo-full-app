from sqlalchemy import and_, func

from todoapp.adapters.database.models import UsersORM
from todoapp.domain.services.users.queries.get_users import GetUsersQueryFilters


def get_predicate(self: GetUsersQueryFilters):
    filter_conditions = []

    if self.username is not None:
        filter_conditions.append(func.lower(UsersORM.username).ilike(f"%{self.username.lower()}%"))

    if self.email is not None:
        filter_conditions.append(func.lower(UsersORM.email).ilike(f"%{self.email.lower()}%"))

    if self.roles is not None:
        filter_conditions.append(UsersORM.role.in_([role.value for role in self.roles]))

    return and_(*filter_conditions) if len(filter_conditions) > 0 else None


GetUsersQueryFilters.get_predicate = get_predicate
