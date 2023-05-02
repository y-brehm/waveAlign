import mock
import unittest
import numpy as np

from wavealign.loudness_processing.lufs_calculator import LUFSCalculator


class TestLUFSCalculator(unittest.TestCase):
    @mock.patch('wavealign.loudness_processing.lufs_calculator.Meter')
    def test_calculate_lufs(self, mock_meter):
        mock_pyln_meter = mock.MagicMock()
        fake_input = np.asarray([0, 1, 2])
        fake_sr = 48000

        mock_meter.return_value = mock_pyln_meter

        LUFSCalculator(fake_sr).calculate_level(fake_input)
        mock_pyln_meter.integrated_loudness.assert_called_once_with(fake_input)
