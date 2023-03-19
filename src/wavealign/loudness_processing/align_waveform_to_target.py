import numpy as np

from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet
from wavealign.loudness_processing.calculation import calculate_gain_difference_to_target


def align_waveform_to_target(audio_spec_set: AudioFileSpecSet, target_lufs: int):
    gain_factor = calculate_gain_difference_to_target(audio_spec_set.original_lufs, target_lufs)
    audio_spec_set.audio_data = np.multiply(audio_spec_set.audio_data, gain_factor)
