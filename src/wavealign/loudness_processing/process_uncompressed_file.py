import numpy as np

from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.data_collection.audio_file_writer import AudioFileWriter
from wavealign.loudness_processing.align_waveform_to_target import (
    align_waveform_to_target,
)


def process_uncompressed_file(
    audio_property_set: AudioPropertySet,
    target_level: int,
    file_path: str,
    audio_data: np.ndarray,
) -> None:
    aligned_audio_data = align_waveform_to_target(
        audio_data, audio_property_set.original_lufs_level, target_level
    )
    AudioFileWriter().write(file_path, aligned_audio_data, audio_property_set.metadata)
