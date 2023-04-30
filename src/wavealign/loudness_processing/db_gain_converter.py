import numpy as np


class DbGainConverter:
    @staticmethod
    def gain_to_db(gain: float) -> float:
        return 20 * np.log10(gain)

    @staticmethod
    def db_to_gain(db_value: float) -> float:
        return 10 ** (db_value / 20)
