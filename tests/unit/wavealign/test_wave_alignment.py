import mock
import unittest

from wavealign.wave_alignment_processor import WaveAlignmentProcessor
from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet


class TestWaveAlignment(unittest.TestCase):
    def setUp(self):
        self.fake_input_path = '/my/dir'
        self.fake_output_path = '/my/out'
        self.fake_target_lufs = -14
        self.fake_audio_data = mock.MagicMock()
        self.fake_audio_file_spec_set = AudioFileSpecSet(
                file_path='/my/dir/fake_file_1.wav',
                audio_data=self.fake_audio_data,
                original_audio_level=7.0,
                metadata=mock.MagicMock()
                )
        self.fake_gain_caluclation_strategy = mock.MagicMock()
        self.mock_normpath = mock.patch(
                'wavealign.wave_alignment_processor.os.path.normpath',
                return_value='/my/dir').start()
        self.mock_find = mock.patch(
                'wavealign.wave_alignment_processor.AudioFileFinder.find',
                return_value=['/my/dir/fake_file_1.wav']).start()
        self.mock_write = mock.patch(
                'wavealign.wave_alignment_processor.AudioFileWriter.write').start()
        self.mock_read = mock.patch(
                'wavealign.wave_alignment_processor.AudioFileReader.read',
                return_value=self.fake_audio_file_spec_set).start()
        self.mock_waveform_alignment = mock.patch(
                'wavealign.wave_alignment_processor.align_waveform_to_target').start()

    def tearDown(self):
        mock.patch.stopall()

    def test_wave_alignment_read_only(self):
        WaveAlignmentProcessor().process(
                input_path=self.fake_input_path,
                output_path='',
                window_size=2,
                gain_calculation_strategy=self.fake_gain_caluclation_strategy,
                target_level=-14,
                read_only=True,
                check_for_clipping=False
                )

        self.mock_normpath.assert_called_once_with(self.fake_input_path)
        self.mock_find.assert_called_once_with(self.mock_normpath.return_value)
        self.mock_read.assert_called_once_with(*self.mock_find.return_value, 2, self.fake_gain_caluclation_strategy)
        self.mock_waveform_alignment.assert_not_called()
        self.mock_write.assert_not_called()

    def test_wave_alignment_write_no_clipping(self):
        WaveAlignmentProcessor().process(
                input_path=self.fake_input_path,
                output_path='',
                window_size=2,
                gain_calculation_strategy=self.fake_gain_caluclation_strategy,
                target_level=-14,
                read_only=False,
                check_for_clipping=False
                )

        self.mock_normpath.assert_called_once_with(self.fake_input_path)
        self.mock_find.assert_called_once_with(self.mock_normpath.return_value)
        self.mock_read.assert_called_once_with(*self.mock_find.return_value, 2, self.fake_gain_caluclation_strategy)
        self.mock_waveform_alignment.assert_called_once_with(
                self.fake_audio_data,
                7.0,
                self.fake_target_lufs
                )
        self.mock_write.assert_called_once_with('/my/dir/fake_file_1.wav',
                                                self.fake_audio_file_spec_set)

    def test_wave_alignment_write_no_clipping_output_path(self):
        try:
            WaveAlignmentProcessor().process(
                    input_path=self.fake_input_path,
                    output_path=self.fake_output_path,
                    window_size=2,
                    gain_calculation_strategy=self.fake_gain_caluclation_strategy,
                    target_level=-14,
                    read_only=False,
                    check_for_clipping=False
                    )
        except Exception:
            self.fail("Unexpected Exception raised by wave_alignment()")

        self.mock_normpath.assert_called_once_with(self.fake_input_path)
        self.mock_find.assert_called_once_with(self.mock_normpath.return_value)
        self.mock_read.assert_called_once_with(*self.mock_find.return_value, 2, self.fake_gain_caluclation_strategy)
        self.mock_waveform_alignment.assert_called_once_with(
                self.fake_audio_data,
                7.0,
                self.fake_target_lufs
                )

        fake_output_file = '/my/out/fake_file_1.wav'
        self.mock_write.assert_called_once_with(
                fake_output_file,
                self.fake_audio_file_spec_set
                )

    @mock.patch('wavealign.wave_alignment_processor.ClippingProcessor.check_for_clipping')
    def test_wave_alignment_detect_clipping(self, mock_check_for_clipping):
        mock_check_for_clipping.return_value = 1

        with self.assertRaises((AssertionError, Exception)):
            WaveAlignmentProcessor().process(
                    input_path=self.fake_input_path,
                    output_path='',
                    window_size=2,
                    gain_calculation_strategy=self.fake_gain_caluclation_strategy,
                    target_level=-14,
                    read_only=False,
                    check_for_clipping=True
                    )

            self.mock_normpath.assert_called_once_with(self.fake_input_path)
            self.mock_find.assert_called_once_with(self.mock_normpath.return_value)
            self.mock_read.assert_called_once_with(*self.mock_find.return_value, 2, self.fake_gain_caluclation_strategy)
            self.mock_waveform_alignment.assert_called_once_with(
                    self.fake_audio_file_spec_set,
                    self.fake_target_lufs
                    )
            mock_check_for_clipping.assert_called_once_with(self.fake_audio_file_spec_set.audio_data)
