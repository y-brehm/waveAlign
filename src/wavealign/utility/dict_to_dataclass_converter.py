import logging
from dataclasses import is_dataclass
from typing import TypeVar, Type, Any

DataClassT = TypeVar("DataClassT", bound=Any)


class DictToDataclassConverter:
    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def process(
        self, class_type: Type[DataClassT], input_dict: dict
    ) -> DataClassT | None:
        if not is_dataclass(class_type):
            self.__logger.debug(
                f"class to convert to has to be of type dataclass. "
                f"Current conversion target {class_type} is of type {type(class_type)}."
            )
            return None

        field_types = {f.name: f.type for f in class_type.__dataclass_fields__.values()}

        for key, value in input_dict.items():
            if key not in field_types:
                self.__logger.debug(
                    f"Additional field '{key}' found in the data dictionary."
                )
                return None

            if hasattr(field_types[key], "__dataclass_fields__"):
                input_dict[key] = self.process(
                    field_types[key], value
                )

            if isinstance(value, list) and hasattr(
                field_types[key].__args__[0], "__dataclass_fields__"
            ):
                nested_cls = field_types[key].__args__[0]
                input_dict[key] = [
                    self.process(nested_cls, v) for v in value
                ]

        return class_type(**input_dict)
