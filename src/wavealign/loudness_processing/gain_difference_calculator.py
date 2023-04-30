from wavealign.loudness_processing.db_gain_converter import DbGainConverter


class GainDifferenceCalculator:
    def __init__(self):
        self.__db_gain_converter = DbGainConverter()

    def calculate_gain_difference_to_target(self,
                                            input_signal_lufs: float,
                                            target_lufs: float
                                            ) -> float:
        gain_difference = target_lufs - input_signal_lufs

        return self.__db_gain_converter.db_to_gain(gain_difference)
