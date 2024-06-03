import os
import logging

from wavealign.data_collection.audio_property_set_generator import (
    AudioPropertySetGenerator,
)
from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_file_finder import AudioFileFinder
from wavealign.data_collection.cache_manager import CacheManager
from wavealign.loudness_processing.window_size import WindowSize

# TODO: Add progress bar #29
# TODO: Move to python 3.11 to enable optional type-hints #26


class AudioPropertySetsReader:
    def __init__(
        self,
        input_path: str,
        window_size: WindowSize,
        cache_manager:  CacheManager | None = None,
    ):
        self.__input_path = input_path
        self.__audio_property_set_generator = AudioPropertySetGenerator(window_size)
        self.__audio_file_finder = AudioFileFinder()
        self.__cache_manager = cache_manager
        self.__logger = logging.getLogger("AUDIO READER")

    def read(self) -> list[AudioPropertySet]:
        audio_property_sets = []
        for file_path in self.__audio_file_finder.find(
            os.path.normpath(self.__input_path)
        ):
            try:
                if self.__cache_manager and self.__cache_manager.is_cached(file_path):
                    self.__logger.info(
                        f"Skipping already processed file: "
                        f"{os.path.basename(file_path)}"
                    )
                    continue

                audio_property_set = self.__audio_property_set_generator.generate(
                    file_path
                )
                audio_property_sets.append(audio_property_set)

            except Exception as e:
                self.__logger.debug("", exc_info=True)
                self.__logger.warning(
                    f"Error processing file: " f"{os.path.basename(file_path)} : {e}"
                )
                continue

        return audio_property_sets
