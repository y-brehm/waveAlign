import numpy as np

from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet
from wavealign.loudness_processing.level_difference_calculator import LevelDifferenceCalculator


class WaveformAligner:
    def __init__(self) -> None:
        self.__gain_difference_calculator = LevelDifferenceCalculator()

    def align_waveform_to_target(
            self,
            audio_file_spec_set: AudioFileSpecSet,
            target_level: int,
            ) -> None:
        gain_factor = self.__gain_difference_calculator.calculate_level_difference_to_target_in_db(
                audio_file_spec_set.original_audio_level,
                target_level
                )
        audio_file_spec_set.audio_data = np.multiply(
                audio_file_spec_set.audio_data,
                gain_factor
                )
