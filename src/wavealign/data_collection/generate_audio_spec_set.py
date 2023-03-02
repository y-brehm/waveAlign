import os

import numpy as np
from librosa import load

from wavealign.loudness_processing.calculation import calculate_lufs
from wavealign.data_collection.audio_spec_set import AudioSpecSet


def generate_audio_spec_set(file_path: str) -> AudioSpecSet:
    audio_data, sample_rate = load(file_path, sr=None, mono=False)
    transposed_audio_data = np.transpose(audio_data)
    original_lufs = calculate_lufs(transposed_audio_data, sample_rate)
    original_file_format = os.path.splitext(file_path)[1]

    return AudioSpecSet(
        file_path=file_path,
        audio_data=transposed_audio_data,
        sample_rate=int(sample_rate),
        original_lufs=original_lufs,
        original_file_extension=original_file_format
    )


