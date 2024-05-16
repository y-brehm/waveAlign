import numpy as np

from wavealign.loudness_processing.db_gain_conversion import db_to_gain


def align_waveform_to_target(
    audio_data: np.ndarray,
    original_audio_level: float,
    target_level: int,
) -> np.ndarray:
    gain_factor = db_to_gain(target_level - original_audio_level)

    return np.multiply(audio_data, gain_factor)
