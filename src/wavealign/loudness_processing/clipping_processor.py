import numpy as np
from wavealign.loudness_processing.peak_calculator import PeakCalculator


class ClippingProcessor:
    def __init__(self):
        self.__peak_calculator = PeakCalculator()

    def check_for_clipping(self, audio_data: np.ndarray) -> None:
        peak_after_processing = self.__peak_calculator.calculate_level(audio_data)
        print(f"new PEAK value after processing: {peak_after_processing} dBFS")
        if peak_after_processing > 0:
            raise Exception(
                f"Clipping detected after processing: {peak_after_processing} dBFS"
            )
