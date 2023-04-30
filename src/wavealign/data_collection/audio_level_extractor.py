import numpy as np

from wavealign.data_collection.gain_calculation_strategy import GainCalculationStrategy
from wavealign.loudness_processing.windowed_level_calculator import WindowedLevelCalculator
from wavealign.loudness_processing.lufs_calculator import LUFSCalculator
from wavealign.loudness_processing.peak_calculator import PeakCalculator
from wavealign.loudness_processing.rms_calculator import RmsCalculator


class AudioLevelExtractor:
    def __init__(self,
                 gain_calculation_strategy: GainCalculationStrategy,
                 sample_rate: int,
                 window_size: int,
                 ) -> None:
        self.__window_size = window_size
        self.__audio_level_calculator = \
            LUFSCalculator(sample_rate) if gain_calculation_strategy == GainCalculationStrategy.LUFS \
            else PeakCalculator() if gain_calculation_strategy == GainCalculationStrategy.PEAK \
            else RmsCalculator()
        self.__windowed_level_calculator = WindowedLevelCalculator(
            self.__window_size,
            sample_rate,
            self.__audio_level_calculator
        )

    def extract(self, audio_data: np.ndarray) -> float:
        if self.__window_size is None:
            audio_level = self.__audio_level_calculator.calculate_level(audio_data)
        else:
            loudest_window = self.__windowed_level_calculator.get_loudest_window(audio_data)
            audio_level = self.__audio_level_calculator.calculate_level(loudest_window)

        return audio_level
