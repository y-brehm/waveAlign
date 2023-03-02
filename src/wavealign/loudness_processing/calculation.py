import numpy as np
from pyloudnorm import Meter


def detect_peak(input_signal: np.ndarray) -> float:
    peak_gain = np.amax([np.amax(buffer) for buffer in input_signal])

    return gain_to_db(peak_gain)


def calculate_gain_difference_to_target(
        input_signal_lufs: float,
        target_lufs: float
) -> float:
    gain_difference = target_lufs - input_signal_lufs

    return db_to_gain(gain_difference)


def calculate_lufs(input_audio: np.ndarray, sample_rate: float) -> float:
    meter = Meter(sample_rate)
    measured_lufs = meter.integrated_loudness(input_audio)

    return measured_lufs


def db_to_gain(db_value: float) -> float:
    return 10 ** (db_value / 20)


def gain_to_db(gain: float) -> float:
    return 20 * np.log10(gain)
