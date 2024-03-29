import numpy as np

from wavealign.loudness_processing.i_audio_level_calculator import IAudioLevelCalculator
from wavealign.loudness_processing.window_cutter import WindowCutter


class WindowedLevelCalculator:
    def __init__(self,
                 window_size: float,
                 sample_rate: int,
                 audio_level_calculator: IAudioLevelCalculator
                 ) -> None:
        self.__window_cutter = WindowCutter(window_size, sample_rate)
        self.__audio_level_calculator = audio_level_calculator

    def get_loudest_window(self, audio_data: np.ndarray) -> np.ndarray:
        windows = self.__window_cutter.cut(audio_data)
        lufs_values = [self.__audio_level_calculator.calculate_level(window) for window in windows]
        loudest_lufs_window_index = lufs_values.index(max(lufs_values))

        return windows[loudest_lufs_window_index]
