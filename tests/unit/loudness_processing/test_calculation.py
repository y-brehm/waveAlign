import mock
import unittest

from wavealign.loudness_processing.calculation import \
    calculate_gain_difference_to_target, detect_peak, calculate_lufs, gain_to_db


class TestCalculation(unittest.TestCase):
    @mock.patch('wavealign.loudness_processing.calculation.np.amax')
    @mock.patch('wavealign.loudness_processing.calculation.gain_to_db')
    def test_detect_peak(self, mock_gain_to_db, mock_amax):
        fake_input = [[0, 1, 2], [3, 4, 5]]
        mock_amax.side_effect = [2, 5, 5]

        detect_peak(fake_input)

        mock_amax.assert_has_calls([
            mock.call([0, 1, 2]),
            mock.call([3, 4, 5]),
            mock.call([2, 5])
        ])

        mock_gain_to_db.assert_called_once_with(5)

    @mock.patch('wavealign.loudness_processing.calculation.db_to_gain')
    def test_calculate_gain_difference_to_target(self, mock_db_to_gain):
        fake_input_lufs = -12
        fake_lufs_target = -10
        fake_output_gain = 1.258925

        mock_db_to_gain.return_value = fake_output_gain

        fake_output = calculate_gain_difference_to_target(
            fake_input_lufs, fake_lufs_target
        )

        mock_db_to_gain.assert_called_once_with(2)
        self.assertEqual(fake_output, fake_output_gain)

    @mock.patch('wavealign.loudness_processing.calculation.Meter')
    def test_calculate_lufs(self, mock_meter):
        mock_pyln_meter = mock.MagicMock()
        fake_input = [0, 1, 2]
        fake_sr = 48000

        mock_meter.return_value = mock_pyln_meter

        calculate_lufs(fake_input, fake_sr)
        mock_pyln_meter.integrated_loudness.assert_called_once_with(fake_input)

    @mock.patch('wavealign.loudness_processing.calculation.np.log10')
    def test_gain_to_db(self, mock_np_log):
        fake_gain = -5
        gain_to_db(fake_gain)
        mock_np_log.assert_called_once_with(fake_gain)
