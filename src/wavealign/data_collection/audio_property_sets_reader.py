import os
import traceback

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

    def read(self) -> tuple[list[AudioPropertySet], list[str]]:
        unprocessed_files = []
        audio_property_sets = []
        for file_path in self.__audio_file_finder.find(
            os.path.normpath(self.__input_path)
        ):
            try:
                if self.__cache_manager and self.__cache_manager.is_cached(file_path):
                    continue

                audio_property_set = self.__audio_property_set_generator.generate(
                    file_path
                )
                audio_property_sets.append(audio_property_set)

            except Exception as e:
                unprocessed_files.append((file_path, str(e)))
                print(f"Error processing file {file_path}: {e}")
                traceback.print_exc()
                continue

        return audio_property_sets, [
            unprocessed_file + ": " + error
            for unprocessed_file, error in unprocessed_files
        ]
