import mock
import unittest
from parameterized import parameterized
from wavealign.wave_alignment import wave_alignment
from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet


class TestWaveAlignment(unittest.TestCase):
    def setUp(self):
        self.fake_audio_file_spec_set = AudioFileSpecSet(
                file_path='/my/dir/fake_file_1.wav',
                audio_data=mock.MagicMock(),
                original_lufs=7.0,
                sample_rate=44100,
                artwork=mock.MagicMock()
                )

    @parameterized.expand([
        ("all parameters set", '/my/dir', '/my/dir', -12, False, True),
        ("no output path", '/my/dir', None, -12, False, True),
        ("clipping occures", '/my/dir', None, -1, False, True)
        ])
    @mock.patch('wavealign.wave_alignment.AudioFileFinder.find')
    @mock.patch('wavealign.wave_alignment.read')
    @mock.patch('wavealign.wave_alignment.align_waveform_to_target')
    @mock.patch('wavealign.wave_alignment.detect_peak')
    @mock.patch('wavealign.wave_alignment.write')
    def test_wave_alignment(
            self,
            test_case,
            fake_input_directory,
            fake_output_directory,
            fake_target_lufs,
            fake_read_only,
            fake_check_for_clipping,
            mock_write,
            mock_detect_peak,
            mock_align_waveform_to_target,
            mock_read,
            mock_find
            ):

        mock_find.return_value = ['/my/dir/fake_file_1.wav']
        mock_read.return_value = self.fake_audio_file_spec_set
        mock_detect_peak.side_effect = [-12, -12, 1]

        wave_alignment(
                fake_input_directory,
                fake_output_directory,
                fake_target_lufs,
                fake_read_only,
                fake_check_for_clipping
                )
        
        mock_find.assert_called_once_with(fake_input_directory)
        mock_read.assert_called_once_with(*mock_find.return_value)
        mock_align_waveform_to_target.assert_called_once_with(
                self.fake_audio_file_spec_set,
                fake_target_lufs
                )
        mock_detect_peak.assert_called_once_with(self.fake_audio_file_spec_set.audio_data)
        mock_write.assert_called_once_with('/my/dir/fake_file_1.wav', self.fake_audio_file_spec_set)
