import mock
import unittest
import numpy as np

from wavealign.loudness_processing.i_audio_level_calculator import IAudioLevelCalculator
from wavealign.loudness_processing.windowed_level_calculator import (
    WindowedLevelCalculator,
)


class TestWindowedLevelCalculator(unittest.TestCase):
    @mock.patch("wavealign.loudness_processing.windowed_level_calculator.WindowCutter")
    def test_get_loudest_window(self, mock_window_cutter):
        window_size = 3
        sample_rate = 44100
        fake_audio_data = np.random.rand(44100 * 2)
        mock_window_cutter.return_value.cut.return_value = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
        ]
        mock_audio_level_calculator = mock.MagicMock(spec=IAudioLevelCalculator)
        mock_audio_level_calculator.calculate_level.side_effect = [0.5, 0.6, 0.7]

        windowed_level_calculator = WindowedLevelCalculator(
            window_size, sample_rate, mock_audio_level_calculator
        )

        result = windowed_level_calculator.get_loudest_window(fake_audio_data)

        mock_window_cutter.assert_called_once_with(window_size, sample_rate)
        mock_window_cutter.return_value.cut.assert_called_once_with(fake_audio_data)
        mock_audio_level_calculator.calculate_level.assert_has_calls(
            [mock.call([0, 1, 2]), mock.call([3, 4, 5]), mock.call([6, 7, 8])]
        )

        self.assertEqual(result, [6, 7, 8])
