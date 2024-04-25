import os
from wavealign.data_collection.audio_property_set_generator import (
    AudioPropertySetGenerator,
)
import traceback

from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_file_finder import AudioFileFinder
from wavealign.loudness_processing.window_size import WindowSize


class AudioPropertySetsReader:
    def __init__(self):
        self.__audio_property_set_generator = AudioPropertySetGenerator()
        self.__audio_file_finder = AudioFileFinder()

    def read(
        self, input_path: str, window_size: WindowSize
    ) -> tuple[list[AudioPropertySet], list[str]]:
        unprocessed_files = []
        audio_property_sets = []
        for file_path in self.__audio_file_finder.find(os.path.normpath(input_path)):
            try:
                audio_property_set = self.__audio_property_set_generator.read(
                    file_path, window_size
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
