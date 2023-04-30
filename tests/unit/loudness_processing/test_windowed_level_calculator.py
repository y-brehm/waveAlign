import mock
import unittest
import numpy as np

from wavealign.loudness_processing.i_audio_level_calculator import IAudioLevelCalculator
from wavealign.loudness_processing.windowed_level_calculator import WindowedLevelCalculator


class TestWindowedLevelCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.window_size = 0.1
        self.sample_rate = 44100
        self.fake_audio_data = np.random.rand(44100 * 2)

        self.mock_window_cutter = mock.patch(
            'wavealign.loudness_processing.windowed_level_calculator.WindowCutter'
        ).start()
        self.mock_window_cutter.return_value.cut.return_value = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.mock_audio_level_calculator = mock.MagicMock(spec=IAudioLevelCalculator)
        self.mock_audio_level_calculator.calculate_level.side_effect = [0.5, 0.6, 0.7]

    def tearDown(self) -> None:
        mock.patch.stopall()

    def test_get_loudest_window(self):
        windowed_level_calculator = WindowedLevelCalculator(
            self.window_size,
            self.sample_rate,
            self.mock_audio_level_calculator
        )

        result = windowed_level_calculator.get_loudest_window(self.fake_audio_data)

        self.mock_window_cutter.assert_called_once_with(self.window_size, self.sample_rate)
        self.mock_window_cutter.return_value.cut.assert_called_once_with(self.fake_audio_data)
        self.mock_audio_level_calculator.calculate_level.assert_has_calls(
            [mock.call([0, 1, 2]), mock.call([3, 4, 5]), mock.call([6, 7, 8])]
        )

        self.assertEqual(result, [6, 7, 8])
