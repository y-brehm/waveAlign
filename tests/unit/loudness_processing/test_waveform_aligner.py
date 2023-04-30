import unittest
import mock

from wavealign.loudness_processing.waveform_aligner import WaveformAligner


class TestWaveformAligner(unittest.TestCase):
    @mock.patch('wavealign.loudness_processing.waveform_aligner.'
                'LevelDifferenceCalculator.calculate_level_difference_to_target_in_db')
    @mock.patch('wavealign.loudness_processing.waveform_aligner.np.multiply')
    def test_align_waveform_to_target(self, mock_np_multiply, mock_calculate_level_difference_to_target):
        fake_audio_file_spec_set = mock.MagicMock()
        fake_audio_data = mock.MagicMock()

        fake_audio_file_spec_set.original_audio_level = -10
        fake_audio_file_spec_set.audio_data = fake_audio_data
        mock_calculate_level_difference_to_target.return_value = 0.63

        WaveformAligner().align_waveform_to_target(fake_audio_file_spec_set, -14)

        mock_calculate_level_difference_to_target.assert_called_once_with(-10, -14)

        mock_np_multiply.assert_called_once_with(fake_audio_data, 0.63)
