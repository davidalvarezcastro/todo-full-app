import attrs
from pydantic import BaseModel


class ConversionAPIDomain(BaseModel):
    def to_domain(self, conversion_type: type) -> any:
        api_dict = self.model_dump()

        for obj_attr, obj_value in vars(self).items():
            if obj_value is None:
                continue

            new_obj_value = self._conversion_api_domain(obj_attr, obj_value, conversion_type)
            new_obj_value = self._conversion_list_api_domain(obj_attr, new_obj_value, conversion_type)
            api_dict[obj_attr] = new_obj_value

        return conversion_type(**api_dict)

    def _conversion_api_domain(self, obj_attr, obj_value, conversion_type):
        if not isinstance(obj_value, ConversionAPIDomain):
            return obj_value

        # Ex: GetTodosQueryFilters | None we are interested to pick the first type to convert
        next_conversion_type = conversion_type.__annotations__[obj_attr].__args__[0]

        return obj_value.to_domain(next_conversion_type)

    def _conversion_list_api_domain(self, obj_attr, obj_value, conversion_type):
        if not isinstance(obj_value, list):
            return obj_value

        new_values = []
        for elem in obj_value:
            new_value = self._conversion_api_domain(obj_attr, elem, conversion_type)
            new_values.append(new_value)

        return new_values

    @classmethod
    def from_domain(cls, attr_obj: attrs.AttrsInstance) -> type:
        return cls(**attrs.asdict(attr_obj))
