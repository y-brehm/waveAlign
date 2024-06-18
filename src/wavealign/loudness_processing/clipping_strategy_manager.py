import os
import logging

from wavealign.loudness_processing.clipping_strategy import ClippingStrategy
from wavealign.loudness_processing.clipping_detected import clipping_detected


class ClippingStrategyManager:
    def __init__(self, clipping_strategy: ClippingStrategy, target_level: int) -> None:
        self.__clipping_strategy = clipping_strategy
        self.__target_level = target_level
        self.__logger = logging.getLogger("CLIPPING STRATEGY MANAGER")

    def should_process(
        self, original_peak_level: float, original_lufs_level: float, file_path: str
    ) -> bool:
        if clipping_detected(
            original_peak_level,
            original_lufs_level,
            self.__target_level,
        ):
            self.__logger.warning(
                f"{os.path.basename(file_path)} was clipped, "
                f"clipping strategy: {str(self.__clipping_strategy)}"
            )
            if self.__clipping_strategy == ClippingStrategy.SKIP:
                return False
            else:
                # TODO: add limiter here #20
                pass

        return True
