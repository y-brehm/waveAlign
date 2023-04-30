import numpy as np
from pyloudnorm import Meter

from wavealign.loudness_processing.i_audio_level_calculator import IAudioLevelCalculator


class LUFSCalculator(IAudioLevelCalculator):
    def __init__(self, sample_rate: int) -> None:
        self.__sample_rate = sample_rate

    def calculate_level(self, audio_data: np.ndarray) -> float:
        meter = Meter(self.__sample_rate)
        measured_lufs = meter.integrated_loudness(audio_data)

        return measured_lufs
