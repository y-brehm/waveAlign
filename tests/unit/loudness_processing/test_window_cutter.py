import unittest
import numpy as np

from wavealign.loudness_processing.window_cutter import WindowCutter


class TestWindowCutter(unittest.TestCase):
    def setUp(self):
        self.sample_rate = 44100
        self.window_size = 0.1  # 100 ms
        self.audio_data = np.random.random(self.sample_rate)
        self.window_cutter = WindowCutter(self.window_size, self.sample_rate)

    def test_cut_no_remaining_samples(self):
        window_size_in_samples = int(self.window_size * self.sample_rate)

        windows = self.window_cutter.cut(self.audio_data[:window_size_in_samples * 4])

        self.assertEqual(len(windows), 4)
        self.assertEqual(windows[0].shape[0], window_size_in_samples)
        self.assertEqual(windows[1].shape[0], window_size_in_samples)

    # This test demonstrates the truncation currently happening in the window cutter.
    def test_cut_with_remaining_samples(self):
        window_cutter = WindowCutter(self.window_size, self.sample_rate)
        window_size_in_samples = int(self.window_size * self.sample_rate)
        extra_samples = 100
        total_samples = window_size_in_samples * 4 + extra_samples

        windows = window_cutter.cut(self.audio_data[:total_samples])

        self.assertEqual(len(windows), 5)
        self.assertEqual(windows[0].shape[0], 3548)
        self.assertEqual(windows[1].shape[0], 3548)
        self.assertEqual(windows[2].shape[0], 3548)

    def test_cut_empty_audio_data(self):
        windows = self.window_cutter.cut(np.array([]))

        self.assertEqual(len(windows), 0)
