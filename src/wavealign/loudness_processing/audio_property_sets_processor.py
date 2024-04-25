import os

from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_file_reader import AudioFileReader
from wavealign.data_collection.audio_file_writer import AudioFileWriter
from wavealign.loudness_processing.clipping_detected import clipping_detected
from wavealign.loudness_processing.clipping_strategy import ClippingStrategy

from wavealign.loudness_processing.align_waveform_to_target import (
    align_waveform_to_target,
)


class AudioPropertySetsProcessor:
    def __init__(self, clipping_strategy: ClippingStrategy):
        self.__audio_file_reader = AudioFileReader()
        self.__audio_file_writer = AudioFileWriter()
        self.__clipping_strategy = clipping_strategy

    def process(
        self,
        audio_property_sets: list[AudioPropertySet],
        target_level: int,
        output_path: str,
    ) -> list[str]:
        clipped_files = []
        for audio_property_set in audio_property_sets:
            if (
                clipping_detected(
                    audio_property_set.original_peak_level,
                    audio_property_set.original_lufs_level,
                    target_level,
                )
                and self.__clipping_strategy == ClippingStrategy.SKIP
            ):
                clipped_files.append(audio_property_set.file_path)
                continue

            # TODO: add limiter here

            audio_data = self.__audio_file_reader.read(audio_property_set.file_path)
            aligned_audio_data = align_waveform_to_target(
                audio_data, audio_property_set.original_lufs_level, target_level
            )

            if not output_path:
                output = audio_property_set.file_path
            else:
                output = os.path.join(
                    output_path, os.path.split(audio_property_set.file_path)[1]
                )
            self.__audio_file_writer.write(
                output, aligned_audio_data, audio_property_set.metadata
            )

        return [
            clipped_file
            + " was clipped, clipping strategy: "
            + str(self.__clipping_strategy.name)
            for clipped_file in clipped_files
        ]
