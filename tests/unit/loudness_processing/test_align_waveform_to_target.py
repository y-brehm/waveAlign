import unittest
import mock

from wavealign.loudness_processing.align_waveform_to_target import align_waveform_to_target
from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet

class TestAlignWaveformToTarget(unittest.TestCase):
    def setUp(self):
        self.fake_audio_file_spec_set = AudioFileSpecSet(
            file_path='/my/dir/fake_file_1.wav',
            audio_data=mock.MagicMock(),
            original_lufs=7.0,
            sample_rate=44100,
            artwork=mock.MagicMock()
            )
        self.fake_target_lufs = -7.0
        self.mock_calculate_gain_difference_to_target = mock.patch(
                'wavealign.loudness_processing.align_waveform_to_target.calculate_gain_difference_to_target',
                return_value=0).start()
        self.mock_np_multiply = mock.patch(
                'wavealign.loudness_processing.align_waveform_to_target.np.multiply',
                return_value=self.fake_audio_file_spec_set.audio_data).start()
                
    
    def tearDown(self):
        self.mock_calculate_gain_difference_to_target.stop()
        self.mock_np_multiply.stop()

    def test_align_waveform_to_target(self):
        align_waveform_to_target(self.fake_audio_file_spec_set, self.fake_target_lufs)

        self.mock_calculate_gain_difference_to_target.assert_called_once_with(
                self.fake_audio_file_spec_set.original_lufs, self.fake_target_lufs 
                )
        self.mock_np_multiply.assert_called_once_with(
                self.fake_audio_file_spec_set.audio_data, 
                self.mock_calculate_gain_difference_to_target.return_value
                )

