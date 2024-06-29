import os
from tqdm import tqdm

from wavealign.caching.levels import Levels
from wavealign.caching.yaml_cache import YamlCache
from wavealign.caching.single_file_cache import SingleFileCache
from wavealign.caching.replace_existing_cache import replace_existing_cache
from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_file_reader import AudioFileReader
from wavealign.data_collection.audio_file_writer import AudioFileWriter
from wavealign.loudness_processing.clipping_strategy_manager import (
    ClippingStrategyManager,
)
from wavealign.loudness_processing.align_waveform_to_target import (
    align_waveform_to_target,
)
from wavealign.loudness_processing.get_new_peak_level import get_new_peak_level


class AudioPropertySetsProcessor:
    def __init__(
        self,
        target_level: int,
        clipping_strategy_manager: ClippingStrategyManager,
        cache_data: YamlCache | None,
    ) -> None:
        self.__audio_file_reader = AudioFileReader()
        self.__audio_file_writer = AudioFileWriter()
        self.__clipping_strategy_manager = clipping_strategy_manager
        self.__target_level = target_level
        self.__cache_data = (
            cache_data if cache_data is not None else YamlCache([], self.__target_level)
        )

    def process(
        self,
        audio_property_sets: list[AudioPropertySet],
        output_path: str,
    ) -> YamlCache:
        progress_bar = tqdm(total=len(audio_property_sets), desc="PROCESSING")
        for audio_property_set in audio_property_sets:
            if not self.__clipping_strategy_manager.should_process(
                audio_property_set.original_peak_level,
                audio_property_set.original_lufs_level,
                audio_property_set.file_path,
            ):
                progress_bar.update(1)
                continue

            audio_data = self.__audio_file_reader.read(audio_property_set.file_path)
            aligned_audio_data = align_waveform_to_target(
                audio_data, audio_property_set.original_lufs_level, self.__target_level
            )

            output_path = self.__generate_output_path(
                audio_property_set.file_path, output_path
            )

            self.__audio_file_writer.write(
                output_path, aligned_audio_data, audio_property_set.metadata
            )

            self.__cache_data.processed_files = replace_existing_cache(
                self.__cache_data.processed_files,
                SingleFileCache(
                    file_path=audio_property_set.file_path,
                    last_modified=os.path.getmtime(audio_property_set.file_path),
                    levels=Levels(
                        lufs=float(self.__target_level),
                        peak=get_new_peak_level(
                            audio_property_set.original_peak_level,
                            audio_property_set.original_lufs_level,
                            self.__target_level,
                        ),
                    ),
                )

            )
            progress_bar.update(1)
        progress_bar.close()

        return self.__cache_data

    def __generate_output_path(self, input_path: str, output_path: str) -> str:
        if not output_path:
            return input_path

        return os.path.join(output_path, os.path.split(input_path)[1])
