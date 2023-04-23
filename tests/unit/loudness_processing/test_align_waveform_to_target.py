import unittest
import mock

from wavealign.loudness_processing.align_waveform_to_target import align_waveform_to_target


class TestAlignWaveformToTarget(unittest.TestCase):
    @mock.patch('wavealign.loudness_processing.align_waveform_to_target.calculate_gain_difference_to_target')
    @mock.patch('wavealign.loudness_processing.align_waveform_to_target.np.multiply')
    def test_align_waveform_to_target(self, mock_np_multiply, mock_calculate_gain_difference_to_target):
        fake_audio_file_spec_set = mock.MagicMock()
        fake_audio_data = mock.MagicMock()

        fake_audio_file_spec_set.original_lufs= -10
        fake_audio_file_spec_set.audio_data = fake_audio_data
        mock_calculate_gain_difference_to_target.return_value = 0.63

        align_waveform_to_target(fake_audio_file_spec_set, -14)

        mock_calculate_gain_difference_to_target.assert_called_once_with(-10, -14)

        mock_np_multiply.assert_called_once_with(fake_audio_data, 0.63)
