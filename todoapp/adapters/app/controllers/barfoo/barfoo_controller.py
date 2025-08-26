import attrs
from fastapi import APIRouter
from pydantic import BaseModel

from todoapp.adapters.app.controllers.common.base_controller import BaseController


class BarFoo(BaseModel):
    msg: str


@attrs.define
class BarFooController(BaseController):
    def _add_url_rules(self, controller: APIRouter) -> None:
        @controller.get(
            "/bar",
            status_code=200,
            # dependencies=[Depends(Authorization())],
        )
        def bar() -> BarFoo:
            return BarFoo(msg="foo")
