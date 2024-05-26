from dataclasses import dataclass


@dataclass(frozen=True)
class Constants:
    granule_length: int = 572


constants = Constants()
