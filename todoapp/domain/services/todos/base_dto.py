from typing import TypeVar

import attrs
from fastapi.types import UnionType

T = TypeVar("T")


@attrs.define
class BaseDTO:
    @classmethod
    def from_model(cls, model: T) -> T:
        filtered = {}
        for cls_attr in cls.__attrs_attrs__:
            value = getattr(model, cls_attr.name, None)

            next_conversion_type = cls.__annotations__[cls_attr.name]

            if type(next_conversion_type) is UnionType:
                next_conversion_type = next_conversion_type.__args__[0]

            if type(next_conversion_type) is BaseDTO:
                filtered[cls_attr.name] = next_conversion_type.from_model(value)
            else:
                filtered[cls_attr.name] = value

        return cls(**filtered)
