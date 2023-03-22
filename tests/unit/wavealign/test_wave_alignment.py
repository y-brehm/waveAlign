import mock
import unittest

from wavealign.wave_alignment import wave_alignment
from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet


class TestWaveAlignment(unittest.TestCase):
    def setUp(self):
        self.fake_input_path = '/my/dir'
        self.fake_output_path = '/my/out'
        self.fake_target_lufs = -14
        
        self.fake_audio_file_spec_set = AudioFileSpecSet(
                file_path='/my/dir/fake_file_1.wav',
                audio_data=mock.MagicMock(),
                original_lufs=7.0,
                sample_rate=44100,
                artwork=mock.MagicMock()
                )


    @mock.patch('wavealign.wave_alignment.read')
    @mock.patch('wavealign.wave_alignment.AudioFileFinder.find')
    def test_wave_alignment_read_only(self, mock_find, mock_read):
        mock_find.return_value = ['/my/dir/fake_file_1.wav']
        mock_read.return_value = self.fake_audio_file_spec_set

        wave_alignment(
                input_path=self.fake_input_path, 
                output_path=None, 
                target_lufs=-14, 
                read_only=True, 
                check_for_clipping=False
                )

        mock_find.assert_called_once_with(self.fake_input_path)
        mock_read.assert_called_once_with(*mock_find.return_value)
        

    @mock.patch('wavealign.wave_alignment.write')
    @mock.patch('wavealign.wave_alignment.align_waveform_to_target')
    @mock.patch('wavealign.wave_alignment.read')
    @mock.patch('wavealign.wave_alignment.AudioFileFinder.find')
    def test_wave_alignment_write_no_clipping(
            self, mock_find, mock_read, mock_align_waveform_to_target, 
            mock_write):
        mock_find.return_value = ['/my/dir/fake_file_1.wav']
        mock_read.return_value = self.fake_audio_file_spec_set
        
        wave_alignment(
                input_path=self.fake_input_path, 
                output_path=None, 
                target_lufs=-14, 
                read_only=False, 
                check_for_clipping=False
                )

        mock_find.assert_called_once_with(self.fake_input_path)
        mock_read.assert_called_once_with(*mock_find.return_value)
        mock_align_waveform_to_target.assert_called_once_with(
                self.fake_audio_file_spec_set, self.fake_target_lufs)
        mock_write.assert_called_once_with(
                self.fake_audio_file_spec_set.file_path,
                self.fake_audio_file_spec_set)


    @mock.patch('wavealign.wave_alignment.write')
    @mock.patch('wavealign.wave_alignment.align_waveform_to_target')
    @mock.patch('wavealign.wave_alignment.read')
    @mock.patch('wavealign.wave_alignment.AudioFileFinder.find')
    def test_wave_alignment_write_no_clipping_output_path(
            self, mock_find, mock_read, mock_align_waveform_to_target, 
            mock_write):
        mock_find.return_value = ['/my/dir/fake_file_1.wav']
        mock_read.return_value = self.fake_audio_file_spec_set
        
        wave_alignment(
                input_path=self.fake_input_path, 
                output_path=self.fake_output_path, 
                target_lufs=-14, 
                read_only=False, 
                check_for_clipping=False
                )

        mock_find.assert_called_once_with(self.fake_input_path)
        mock_read.assert_called_once_with(*mock_find.return_value)
        mock_align_waveform_to_target.assert_called_once_with(
                self.fake_audio_file_spec_set, self.fake_target_lufs)

        fake_output_file = '/my/out/fake_file_1.wav'
        mock_write.assert_called_once_with(
                fake_output_file,
                self.fake_audio_file_spec_set)


    @mock.patch('wavealign.wave_alignment.detect_peak')
    @mock.patch('wavealign.wave_alignment.align_waveform_to_target')
    @mock.patch('wavealign.wave_alignment.read')
    @mock.patch('wavealign.wave_alignment.AudioFileFinder.find')
    def test_wave_alignment_detect_clipping(
            self, mock_find, mock_read, mock_align_waveform_to_target, 
            mock_detect_peak):
        mock_find.return_value = ['/my/dir/fake_file_1.wav']
        mock_read.return_value = self.fake_audio_file_spec_set
        mock_detect_peak.return_value = 1
       
        with self.assertRaises((AssertionError, Exception)):
            wave_alignment(
                    input_path=self.fake_input_path, 
                    output_path=None, 
                    target_lufs=-14, 
                    read_only=False, 
                    check_for_clipping=True
                    )

            mock_find.assert_called_once_with(self.fake_input_path)
            mock_read.assert_called_once_with(*mock_find.return_value)
            mock_align_waveform_to_target.assert_called_once_with(
                    self.fake_audio_file_spec_set, self.fake_target_lufs)
            mock_detect_peak.assert_called_once_with(
                    self.fake_audio_file_spec_set.audio_data)
