import numpy as np

from wavealign.loudness_processing.i_audio_level_calculator import IAudioLevelCalculator
from wavealign.loudness_processing.db_gain_converter import DbGainConverter


class PeakCalculator(IAudioLevelCalculator):
    def __init__(self):
        self.__db_gain_converter = DbGainConverter()

    def calculate_level(self, audio_data: np.ndarray) -> float:
        return self.__db_gain_converter.gain_to_db(np.max(np.abs(audio_data)))

