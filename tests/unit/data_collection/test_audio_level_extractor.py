import unittest

import mock
import numpy as np

from wavealign.data_collection.gain_calculation_strategy import GainCalculationStrategy
from wavealign.data_collection.audio_level_extractor import AudioLevelExtractor
from wavealign.loudness_processing.lufs_calculator import LUFSCalculator
from wavealign.loudness_processing.peak_calculator import PeakCalculator
from wavealign.loudness_processing.rms_calculator import RmsCalculator
from wavealign.loudness_processing.windowed_level_calculator import WindowedLevelCalculator


class TestAudioLevelExtractor(unittest.TestCase):
    def setUp(self):
        self.sample_rate = 44100
        self.window_size = 2
        self.fake_audio_data = np.random.random(self.sample_rate)

    def test_extract_lufs(self):
        gain_calculation_strategy = GainCalculationStrategy.LUFS
        audio_level_extractor = AudioLevelExtractor(gain_calculation_strategy, self.sample_rate, self.window_size)

        audio_level_calculator = LUFSCalculator(self.sample_rate)
        windowed_level_calculator = WindowedLevelCalculator(self.window_size, self.sample_rate, audio_level_calculator)
        loudest_window = windowed_level_calculator.get_loudest_window(self.fake_audio_data)
        expected_value = audio_level_calculator.calculate_level(loudest_window)

        self.assertAlmostEqual(audio_level_extractor.extract(self.fake_audio_data), expected_value, places=6)

    def test_extract_peak(self):
        gain_calculation_strategy = GainCalculationStrategy.PEAK
        audio_level_extractor = AudioLevelExtractor(gain_calculation_strategy, self.sample_rate, self.window_size)

        audio_level_calculator = PeakCalculator()
        windowed_level_calculator = WindowedLevelCalculator(self.window_size, self.sample_rate, audio_level_calculator)
        loudest_window = windowed_level_calculator.get_loudest_window(self.fake_audio_data)
        expected_value = audio_level_calculator.calculate_level(loudest_window)

        self.assertAlmostEqual(audio_level_extractor.extract(self.fake_audio_data), expected_value, places=6)

    def test_extract_rms(self):
        gain_calculation_strategy = GainCalculationStrategy.RMS
        audio_level_extractor = AudioLevelExtractor(gain_calculation_strategy, self.sample_rate, self.window_size)

        audio_level_calculator = RmsCalculator()
        windowed_level_calculator = WindowedLevelCalculator(self.window_size, self.sample_rate, audio_level_calculator)
        loudest_window = windowed_level_calculator.get_loudest_window(self.fake_audio_data)
        expected_value = audio_level_calculator.calculate_level(loudest_window)

        self.assertAlmostEqual(audio_level_extractor.extract(self.fake_audio_data), expected_value, places=6)

    @mock.patch('wavealign.data_collection.audio_level_extractor.LUFSCalculator')
    def test_extract_audio_level_without_window(self, mock_audio_level_calculator):
        gain_calculation_strategy = GainCalculationStrategy.LUFS
        mock_audio_level_calculator.return_value.calculate_level.return_value = 1.0
        audio_level_extractor = AudioLevelExtractor(gain_calculation_strategy, self.sample_rate, None)

        result = audio_level_extractor.extract(self.fake_audio_data)

        mock_audio_level_calculator.return_value.calculate_level.assert_called_once_with(self.fake_audio_data)
        self.assertEqual(result, 1.0)

    @mock.patch('wavealign.data_collection.audio_level_extractor.WindowedLevelCalculator')
    @mock.patch('wavealign.data_collection.audio_level_extractor.LUFSCalculator')
    def test_extract_audio_level_with_window(self, mock_audio_level_calculator, mock_windowed_level_calculator):
        gain_calculation_strategy = GainCalculationStrategy.LUFS

        mock_windowed_level_calculator.return_value.get_loudest_window.return_value = [1, 2, 3]
        mock_audio_level_calculator.return_value.calculate_level.return_value = 2.0

        audio_level_extractor = AudioLevelExtractor(gain_calculation_strategy, self.sample_rate, window_size=2)

        result = audio_level_extractor.extract(self.fake_audio_data)

        mock_windowed_level_calculator.return_value.get_loudest_window.assert_called_once_with(self.fake_audio_data)
        mock_audio_level_calculator.return_value.calculate_level.assert_called_once_with([1, 2, 3])
        self.assertEqual(result, 2.0)
