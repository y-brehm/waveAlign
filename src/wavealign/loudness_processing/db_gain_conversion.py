import numpy as np


def gain_to_db(gain: float) -> float:
    return 20 * np.log10(gain) if gain != 0 else -np.inf


def db_to_gain(db_value: float) -> float:
    return 10 ** (db_value / 20)
