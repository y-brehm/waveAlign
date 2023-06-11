from time import sleep
from numpy import array, random, zeros
import matplotlib.pyplot as plt


class Limiter:
    def __init__(self, attack_coeff, release_coeff, delay, threshold):
        self.delay_index = 0
        self.envelope = 0
        self.gain = 1
        self.delay = delay
        self.delay_line = zeros(delay)
        self.release_coeff = release_coeff
        self.attack_coeff = attack_coeff
        self.threshold = threshold

    def limit(self, signal):
        for idx, sample in enumerate(signal):
            self.delay_line[self.delay_index] = sample
            self.delay_index = (self.delay_index + 1) % self.delay

            # calculate an envelope of the signal
            target_gain = self.get_envelope(sample)

            # have self.gain go towards a desired limiter gain
            self.gain = self.gain*self.attack_coeff + target_gain*(1-self.attack_coeff)

            # limit the delayed signal
            signal[idx] = self.delay_line[self.delay_index] * self.gain

        return signal

    def get_envelope(self, sample):
        self.envelope = max(abs(sample), self.envelope*self.release_coeff)

        if self.envelope > self.threshold:
            return self.threshold / self.envelope

        return 1.0
