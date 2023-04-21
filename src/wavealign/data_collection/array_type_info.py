from dataclasses import dataclass


@dataclass
class ArrayTypeInfo:
    abs_max: int
    offset: int
    min: int
    max: int
