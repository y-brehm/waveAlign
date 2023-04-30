import mock
import unittest
import numpy as np

from wavealign.loudness_processing.peak_calculator import PeakCalculator


class TestPeakCalculator(unittest.TestCase):
    @mock.patch('wavealign.loudness_processing.peak_calculator.np.abs')
    @mock.patch('wavealign.loudness_processing.peak_calculator.np.max')
    @mock.patch('wavealign.loudness_processing.peak_calculator.DbGainConverter.gain_to_db')
    def test_detect_peak(self, mock_gain_to_db, mock_np_max, mock_np_abs):
        fake_input = np.asarray([[0, -1, 2], [3, 4, -5]])

        mock_np_abs.return_value = [[0, 1, 2], [3, 4, 5]]
        mock_np_max.return_value = 5

        PeakCalculator().calculate_level(fake_input)

        mock_np_abs.assert_called_once_with(fake_input)
        mock_np_max.assert_called_once_with([[0, 1, 2], [3, 4, 5]])
        mock_gain_to_db.assert_called_once_with(5)

    def test_result_full_scale(self):
        fake_input = np.asarray([[0, -0.1, 1], [0, -0.3, -0.9]])

        result = PeakCalculator().calculate_level(fake_input)

        self.assertAlmostEqual(result, 0.0)

    def test_result_negative_max(self):
        fake_input = np.asarray([[0, -0.1, 0.3], [0, -0.3, -0.707946]])

        result = PeakCalculator().calculate_level(fake_input)

        self.assertAlmostEqual(result, -3.0, places=5)

    def test_result_positive_max(self):
        fake_input = np.asarray([[0, -0.1, 0.3], [0, -0.3, 0.707946]])

        result = PeakCalculator().calculate_level(fake_input)

        self.assertAlmostEqual(result, -3.0, places=5)
