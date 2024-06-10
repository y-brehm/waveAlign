import os
import logging
from tqdm import tqdm

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
        self.__cache_data = cache_data
        self.__logger = logging.getLogger("AUDIO PROCESSOR")

    def process(
        self,
        audio_property_sets: list[AudioPropertySet],
        target_level: int,
        output_path: str,
    ) -> dict:
        progress_bar = tqdm(total=len(audio_property_sets), desc="PROCESSING")
        for audio_property_set in audio_property_sets:
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
                continue
            # TODO: add limiter here #20

            audio_data = self.__audio_file_reader.read(audio_property_set.file_path)
            aligned_audio_data = align_waveform_to_target(
                audio_data, audio_property_set.original_lufs_level, target_level
            )

            output = self.__generate_output_path(
                audio_property_set.file_path, output_path
            )

            self.__audio_file_writer.write(
                output, aligned_audio_data, audio_property_set.metadata
            )

            self.__cache_data[audio_property_set.file_path] = (
                audio_property_set.last_modified
            )
            progress_bar.update(1)

        self.__cache_data["target_level"] = target_level
        progress_bar.close()

        return self.__cache_data

    def __generate_output_path(self, input_path: str, output_path: str) -> str:
        if not output_path:
            return input_path

        return os.path.join(output_path, os.path.split(input_path)[1])
