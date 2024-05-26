from numpy import ndarray

from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_file_writer import AudioFileWriter
from wavealign.loudness_processing.align_waveform_to_target import (
    align_waveform_to_target,
)


class UncompressedFileProcessor:
    def __init__(self) -> None:
        self.__audio_file_writer = AudioFileWriter()

    def process(
        self,
        audio_property_set: AudioPropertySet,
        target_level: int,
        file_path: str,
        audio_data: ndarray,
    ) -> None:
        aligned_audio_data = align_waveform_to_target(
            audio_data, audio_property_set.original_lufs_level, target_level
        )
        self.__audio_file_writer.write(
            file_path, aligned_audio_data, audio_property_set.metadata
        )
