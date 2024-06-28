import os
import logging
import concurrent.futures
from tqdm import tqdm

from wavealign.data_collection.audio_property_set_generator import (
    AudioPropertySetGenerator,
)
from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_file_finder import AudioFileFinder
from wavealign.data_collection.cache_manager import CacheManager
from wavealign.loudness_processing.window_size import WindowSize

# TODO: Move to python 3.11 to enable optional type-hints #26


class AudioPropertySetsReader:
    def __init__(
        self,
        input_path: str,
        window_size: WindowSize,
        cache_manager: CacheManager | None = None,
    ):
        self.__input_path = input_path
        self.__audio_property_set_generator = AudioPropertySetGenerator(window_size)
        self.__cache_manager = cache_manager
        self.__logger = logging.getLogger("AUDIO READER")
        self.files_to_process = AudioFileFinder().find(
            os.path.normpath(self.__input_path)
        )
        self.__audio_property_sets = []

    def read(self) -> list[AudioPropertySet]:
        self.__print_files_to_process(self.files_to_process)
        progress_bar = tqdm(total=len(self.files_to_process), desc="READING")

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(self._compile_audio_property_sets, file_to_process)
                for file_to_process in self.files_to_process
            ]

            for future in concurrent.futures.as_completed(futures):
                # TODO: try except block?
                self.__audio_property_sets.append(future.result())
                progress_bar.update(1)

        progress_bar.close()

        return self.__audio_property_sets

    def _compile_audio_property_sets(self, file_path: str) -> AudioPropertySet | None:
        try:
            if self.__cache_manager and self.__cache_manager.is_cached(file_path):
                self.__logger.info(
                    f"Skipping already processed file: "
                    f"{os.path.basename(file_path)}"
                )

            return self.__audio_property_set_generator.generate(file_path)

        except Exception:
            self.__logger.warning(
                f"Error processing file: " f"{os.path.basename(file_path)}"
            )
            self.__logger.debug("", exc_info=True)

    def __print_files_to_process(self, files_to_process: list[str]) -> None:
        print(f"### OVERALL FILES TO PROCESS: {len(files_to_process)} ###\n")
