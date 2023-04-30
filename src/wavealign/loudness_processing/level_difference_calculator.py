from wavealign.loudness_processing.db_gain_converter import DbGainConverter


class LevelDifferenceCalculator:
    def __init__(self):
        self.__db_gain_converter = DbGainConverter()

    def calculate_level_difference_to_target_in_db(self,
                                                   input_signal_lufs: float,
                                                   target_lufs: float
                                                   ) -> float:
        gain_difference = target_lufs - input_signal_lufs

        return self.__db_gain_converter.db_to_gain(gain_difference)
