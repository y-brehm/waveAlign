import os

from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_property_sets_reader import AudioPropertySetsReader
from wavealign.data_collection.audio_property_sets_analyzer import (
    AudioPropertySetsAnalyzer,
)
from wavealign.loudness_processing.window_size import WindowSize


class WaveAlignmentReader:
    def __init__(self, input_path: str, window_size: WindowSize) -> None:
        self.__window_size: WindowSize = window_size
        self.__audio_property_sets_reader = AudioPropertySetsReader(
            input_path=input_path,
            window_size=window_size,
        )
        self.__audio_property_sets_analyzer = AudioPropertySetsAnalyzer()

    def read(self) -> tuple[list[AudioPropertySet], int]:
        audio_property_sets = self.__audio_property_sets_reader.read()
        library_dependent_target_level = (
            self.__audio_property_sets_analyzer.detect_target_value(audio_property_sets)
        )
        self.__print_audio_properties(
            audio_property_sets, library_dependent_target_level
        )

        return audio_property_sets, library_dependent_target_level

    def __print_audio_properties(
        self,
        audio_property_sets: list[AudioPropertySet],
        library_dependent_target_level: int,
    ) -> None:
        for audio_property_set in audio_property_sets:
            print(
                f"FILE: {os.path.basename(audio_property_set.file_path)} "
                f"ORIGINAL LUFS: {audio_property_set.original_lufs_level:.2f} "
                f"dB {self.__window_size.name} "
                f"ORIGINAL PEAK: {audio_property_set.original_peak_level:.2f}"
            )
        print(
            f"Library dependent target level: "
            f"{library_dependent_target_level} "
            f"dB {self.__window_size.name}"
        )
