import mock
import unittest

from src.wavealign.wave_alignment import wave_alignment
from src.wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet


class TestWaveAlignment(unittest.TestCase):
    def setUp(self):
        self.fake_input_path = '/my/dir'
        self.fake_output_path = '/my/out'
        self.fake_target_lufs = -14

        self.fake_audio_file_spec_set = AudioFileSpecSet(
                file_path='/my/dir/fake_file_1.wav',
                audio_data=mock.MagicMock(),
                original_lufs=7.0,
                metadata=mock.MagicMock()
                )

        self.mock_normpath = mock.patch(
                'src.wavealign.wave_alignment.os.path.normpath',
                return_value='/my/dir').start()
        self.mock_find = mock.patch(
                'src.wavealign.wave_alignment.AudioFileFinder.find',
                return_value=['/my/dir/fake_file_1.wav']).start()
        self.mock_write = mock.patch(
                'src.wavealign.wave_alignment.AudioFileWriter.write').start()
        self.mock_read = mock.patch(
                'src.wavealign.wave_alignment.AudioFileReader.read',
                return_value=self.fake_audio_file_spec_set).start()
        self.mock_align_waveform_to_target = mock.patch(
                'src.wavealign.wave_alignment.align_waveform_to_target').start()

    def tearDown(self):
        mock.patch.stopall()

    def test_wave_alignment_read_only(self):
        wave_alignment(
                input_path=self.fake_input_path,
                output_path="",
                target_lufs=-14,
                read_only=True,
                check_for_clipping=False
                )

        self.mock_normpath.assert_called_once_with(self.fake_input_path)
        self.mock_find.assert_called_once_with(self.mock_normpath.return_value)
        self.mock_read.assert_called_once_with(*self.mock_find.return_value)
        self.mock_align_waveform_to_target.assert_not_called()
        self.mock_write.assert_not_called()

    def test_wave_alignment_write_no_clipping(self):
        wave_alignment(
                input_path=self.fake_input_path,
                output_path="",
                target_lufs=-14,
                read_only=False,
                check_for_clipping=False
                )

        self.mock_normpath.assert_called_once_with(self.fake_input_path)
        self.mock_find.assert_called_once_with(self.mock_normpath.return_value)
        self.mock_read.assert_called_once_with(*self.mock_find.return_value)
        self.mock_align_waveform_to_target.assert_called_once_with(
                self.fake_audio_file_spec_set,
                self.fake_target_lufs
                )
        self.mock_write.assert_called_once_with('fake_file_1.wav',
                                                self.fake_audio_file_spec_set)

    def test_wave_alignment_write_no_clipping_output_path(self):
        try:
            wave_alignment(
                    input_path=self.fake_input_path,
                    output_path=self.fake_output_path,
                    target_lufs=-14,
                    read_only=False,
                    check_for_clipping=False
                    )
        except Exception:
            self.fail("Unexpected Exception raised by wave_alignment()")

        self.mock_normpath.assert_called_once_with(self.fake_input_path)
        self.mock_find.assert_called_once_with(self.mock_normpath.return_value)
        self.mock_read.assert_called_once_with(*self.mock_find.return_value)
        self.mock_align_waveform_to_target.assert_called_once_with(
                self.fake_audio_file_spec_set,
                self.fake_target_lufs
                )

        fake_output_file = '/my/out/fake_file_1.wav'
        self.mock_write.assert_called_once_with(
                fake_output_file,
                self.fake_audio_file_spec_set
                )

    @mock.patch('src.wavealign.wave_alignment.detect_peak')
    def test_wave_alignment_detect_clipping(self, mock_detect_peak):
        mock_detect_peak.return_value = 1

        with self.assertRaises((AssertionError, Exception)):
            wave_alignment(
                    input_path=self.fake_input_path,
                    output_path="",
                    target_lufs=-14,
                    read_only=False,
                    check_for_clipping=True
                    )

            self.mock_normpath.assert_called_once_with(self.fake_input_path)
            self.mock_find.assert_called_once_with(self.mock_normpath.return_value)
            self.mock_read.assert_called_once_with(*self.mock_find.return_value)
            self.mock_align_waveform_to_target.assert_called_once_with(
                    self.fake_audio_file_spec_set,
                    self.fake_target_lufs
                    )
            mock_detect_peak.assert_called_once_with(self.fake_audio_file_spec_set.audio_data)
