from time import sleep
from numpy import array, random, zeros, copy
import matplotlib.pyplot as plt
from wavealign.dsp.limiter import Limiter
import unittest


class TestLimiter(unittest.TestCase):
    def generate_test_signal(self):
        sample_rate = 44100
        signal_length_seconds = 1
        signal = array(random.rand(sample_rate * signal_length_seconds) * 2 - 1)
        signal[:int(signal_length_seconds * sample_rate / 3)] *= 0.1
        signal[int(signal_length_seconds * sample_rate * 2 / 3):] *= 0.1

        return signal

    def test_limiter(self):
        threshold = 0.5
        delay = 40
        release_coeff = 0.9995
        attack_coeff = 0.9

        signal = self.generate_test_signal()
        original_signal = copy(signal)

        limiter = Limiter(attack_coeff, release_coeff, delay, threshold)
        limited_signal = limiter.limit(signal)

        plt.figure()
        plt.plot(original_signal, label='original signal')
        plt.plot(limited_signal, label='limited signal')
        plt.legend()
        plt.show()
