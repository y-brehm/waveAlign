import numpy as np

from wavealign.loudness_processing.i_audio_level_calculator import IAudioLevelCalculator
from wavealign.loudness_processing.db_gain_conversion import gain_to_db


class RmsCalculator(IAudioLevelCalculator):
    def calculate_level(self, audio_data: np.ndarray) -> float:
        return gain_to_db(np.sqrt(np.mean(audio_data ** 2)))
