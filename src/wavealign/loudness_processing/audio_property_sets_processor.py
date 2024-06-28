import os
import logging

from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_file_reader import AudioFileReader
from wavealign.data_collection.audio_file_writer import AudioFileWriter
from wavealign.loudness_processing.clipping_detected import clipping_detected
from wavealign.loudness_processing.clipping_strategy import ClippingStrategy

from wavealign.loudness_processing.align_waveform_to_target import (
    align_waveform_to_target,
)

# TODO: switch from dict to dataclass for cache_data #30
# TODO: write more data to cache_data (e.g. original peak level, original lufs level) #30


class AudioPropertySetsProcessor:
    def __init__(self, clipping_strategy: ClippingStrategy, cache_data: dict):
        self.__audio_file_reader = AudioFileReader()
        self.__audio_file_writer = AudioFileWriter()
        self.__clipping_strategy = clipping_strategy
        # TODO: Remove cache data?
        self.__cache_data = cache_data
        self.__logger = logging.getLogger("AUDIO PROCESSOR")

    def process(
        self,
        audio_property_set: AudioPropertySet,
        target_level: int,
        output_path: str,
    ) -> tuple[str, float]:
        if (
            clipping_detected(
                audio_property_set.original_peak_level,
                audio_property_set.original_lufs_level,
                target_level,
            )
            and self.__clipping_strategy == ClippingStrategy.SKIP
        ):
            self.__logger.warning(
                f"{os.path.basename(audio_property_set.file_path)} was clipped, "
                f"clipping strategy: {str(self.__clipping_strategy)}"
            )
        # TODO: add limiter here #20

        audio_data = self.__audio_file_reader.read(audio_property_set.file_path)
        aligned_audio_data = align_waveform_to_target(
            audio_data, audio_property_set.original_lufs_level, target_level
        )

        output = self.__generate_output_path(audio_property_set.file_path, output_path)

        self.__audio_file_writer.write(
            output, aligned_audio_data, audio_property_set.metadata
        )

        return audio_property_set.file_path, audio_property_set.last_modified

    def __generate_output_path(self, input_path: str, output_path: str) -> str:
        if not output_path:
            return input_path

        return os.path.join(output_path, os.path.split(input_path)[1])
