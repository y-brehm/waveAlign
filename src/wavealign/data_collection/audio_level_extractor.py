import numpy as np

from wavealign.data_collection.gain_calculation_strategy import GainCalculationStrategy
from wavealign.loudness_processing.window_size import WindowSize
from wavealign.loudness_processing.windowed_level_calculator import WindowedLevelCalculator
from wavealign.loudness_processing.lufs_calculator import LUFSCalculator
from wavealign.loudness_processing.peak_calculator import PeakCalculator


class AudioLevelExtractor:
    def __init__(self,
                 gain_calculation_strategy: GainCalculationStrategy,
                 sample_rate: int,
                 window_size: WindowSize,
                 ) -> None:
        self.__sample_rate = sample_rate
        self.__window_size = window_size
        self.__audio_level_calculator = self.__select_level_calculator(gain_calculation_strategy)

    def extract(self, audio_data: np.ndarray) -> float:
        # TODO: find out with this has to be .value
        if self.__window_size.value == WindowSize.LUFS_I.value:
            return self.__audio_level_calculator.calculate_level(audio_data)

        windowed_level_calculator = WindowedLevelCalculator(
            self.__window_size,
            self.__sample_rate,
            self.__audio_level_calculator
        )
        loudest_window = windowed_level_calculator.get_loudest_window(audio_data)

        return self.__audio_level_calculator.calculate_level(loudest_window)

    def __select_level_calculator(self, gain_calculation_strategy: GainCalculationStrategy):
        if gain_calculation_strategy == GainCalculationStrategy.LUFS:
            return LUFSCalculator(self.__sample_rate)
        else:
            return PeakCalculator()
