from typing import Self


class WarningStatusSingleton:
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(WarningStatusSingleton, cls).__new__(cls)
            cls._instance.warning_counts = False
        return cls._instance

    def set_warning_counts(self) -> None:
        self.warning_counts = True

    def get_warning_counts(self) -> bool:
        return self.warning_counts
