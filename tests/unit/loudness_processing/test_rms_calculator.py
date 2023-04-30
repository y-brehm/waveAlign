import unittest
import numpy as np
import mock

from wavealign.loudness_processing.rms_calculator import RmsCalculator


class TestRmsCalculator(unittest.TestCase):
    @mock.patch('wavealign.loudness_processing.rms_calculator.np.mean')
    @mock.patch('wavealign.loudness_processing.rms_calculator.np.sqrt')
    @mock.patch('wavealign.loudness_processing.rms_calculator.DbGainConverter.gain_to_db')
    def test_calculate_rms(self, mock_gain_to_db, mock_np_sqrt, mock_np_mean):
        fake_input = np.asarray([[0, -1, 2], [3, 4, -5]])

        mock_np_mean.return_value = 9
        mock_np_sqrt.return_value = 3

        RmsCalculator().calculate_level(fake_input)

        np.testing.assert_array_equal(mock_np_mean.call_args[0][0], fake_input ** 2)
        mock_np_sqrt.assert_called_once_with(9)
        mock_gain_to_db.assert_called_once_with(3)

    def test_result_full_scale(self):
        fake_input = np.asarray([[0, -0.1, 1], [0, -0.3, -0.9]])

        result = RmsCalculator().calculate_level(fake_input)

        self.assertAlmostEqual(result, -4.971178831359159, places=6)

    def test_result_negative_max(self):
        fake_input = np.asarray([[0, -0.1, 0.3], [0, -0.3, -0.707946]])

        result = RmsCalculator().calculate_level(fake_input)

        self.assertAlmostEqual(result, -9.385553505262363, places=6)

    def test_result_positive_max(self):
        fake_input = np.asarray([[0, -0.1, 0.3], [0, -0.3, 0.707946]])

        result = RmsCalculator().calculate_level(fake_input)

        self.assertAlmostEqual(result, -9.385553505262363, places=6)
