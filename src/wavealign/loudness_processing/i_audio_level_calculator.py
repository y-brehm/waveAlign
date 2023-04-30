from numpy import ndarray
from abc import ABC, abstractmethod


class IAudioLevelCalculator(ABC):
    @abstractmethod
    def calculate_level(self, audio_data: ndarray) -> float:
        pass
