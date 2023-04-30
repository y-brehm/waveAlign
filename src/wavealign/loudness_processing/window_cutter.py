import math
import numpy as np


class WindowCutter:
    def __init__(self, window_size: float, sample_rate: int) -> None:
        self.__window_size = window_size
        self.__sample_rate = sample_rate

    def cut(self,
            audio_data: np.ndarray,
            ) -> list[np.ndarray]:
        window_size_in_samples = math.ceil(self.__window_size * self.__sample_rate)
        window_count = math.ceil(len(audio_data) / window_size_in_samples)

        return np.array_split(audio_data, window_count)
