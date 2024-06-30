import os
import logging
from tqdm import tqdm

from wavealign.caching.levels_cache_finder import LevelsCacheFinder
from wavealign.data_collection.audio_property_set_generator import (
    AudioPropertySetGenerator,
)
from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_file_finder import AudioFileFinder
from wavealign.caching.cache_validator import CacheValidator
from wavealign.loudness_processing.window_size import WindowSize


class AudioPropertySetsReader:
    def __init__(
        self,
        input_path: str,
        window_size: WindowSize,
        cache_validator: CacheValidator | None = None,
        levels_cache_finder: LevelsCacheFinder | None = None,
    ):
        self.__input_path = input_path
        self.__audio_property_set_generator = AudioPropertySetGenerator(
            window_size, levels_cache_finder
        )
        self.__cache_validator = cache_validator
        self.__logger = logging.getLogger("AUDIO READER")
        self.files_to_process = AudioFileFinder().find(
            os.path.normpath(self.__input_path)
        )

    def read(self) -> list[AudioPropertySet]:
        audio_property_sets = []
        self.__print_files_to_process(self.files_to_process)
        progress_bar = tqdm(total=len(self.files_to_process), desc="READING")

        for file_path in self.files_to_process:
            try:
                if self.__cache_validator and self.__cache_validator.is_cached(file_path):
                    self.__logger.info(
                        f"Skipping already processed file: "
                        f"{os.path.basename(file_path)}"
                    )
                    progress_bar.update(1)
                    continue

                audio_property_set = self.__audio_property_set_generator.generate(
                    file_path
                )
                audio_property_sets.append(audio_property_set)
                progress_bar.update(1)

            except Exception:
                self.__logger.warning(
                    f"Error processing file: " f"{os.path.basename(file_path)}"
                )
                self.__logger.debug("", exc_info=True)
                progress_bar.update(1)
                continue

        progress_bar.close()

        return audio_property_sets

    def __print_files_to_process(self, files_to_process: list[str]) -> None:
        print(f"### OVERALL FILES TO PROCESS: {len(files_to_process)} ###\n")
