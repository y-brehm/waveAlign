import mock
import unittest

from wavealign.data_collection.audio_file_reader import AudioFileReader
from wavealign.data_collection.audio_metadata import AudioMetadata


class TestAudioFileReader(unittest.TestCase):
    def setUp(self):
        self.mock_audio_data = mock.MagicMock()
        self.mock_artwork = mock.MagicMock()
        self.mock_metadata = AudioMetadata(
            num_channels=2,
            artwork=self.mock_artwork,
            codec_name='eva01',
            bit_rate=16,
            sample_rate=44100)

        self.mock_pcm_float_converter = mock.patch(
            'wavealign.data_collection.audio_file_reader.PcmFloatConverter').start()
        self.mock_extract = mock.patch(
            'wavealign.data_collection.audio_file_reader.MetaDataExtractor.extract').start()
        self.mock_calculate_lufs = mock.patch(
            'wavealign.data_collection.audio_file_reader.calculate_lufs').start()
        self.mock_read = mock.patch(
            'wavealign.data_collection.audio_file_reader.audio.read').start()

        self.mock_extract.return_value = self.mock_metadata
        self.mock_read.return_value = (44100, self.mock_audio_data)
        self.mock_calculate_lufs.return_value = -15

    def tearDown(self):
        mock.patch.stopall()

    def test_read(self):
        self.mock_pcm_float_converter.return_value.is_pcm_encoded.return_value = False

        file_spec_set = AudioFileReader().read('some_path')

        self.assertEqual(file_spec_set.file_path, 'some_path')
        self.assertEqual(file_spec_set.audio_data, self.mock_audio_data)
        self.assertAlmostEqual(file_spec_set.original_lufs, -15)
        self.assertEqual(file_spec_set.metadata, self.mock_metadata)
        self.mock_pcm_float_converter.return_value.pcm_to_float.assert_not_called()

    def test_read_with_conversion(self):
        mock_audio_data_converted = mock.MagicMock()
        self.mock_pcm_float_converter.return_value.pcm_to_float.return_value = mock_audio_data_converted
        self.mock_pcm_float_converter.return_value.is_pcm_encoded.return_value = True

        file_spec_set = AudioFileReader().read('some_path')

        self.assertEqual(file_spec_set.file_path, 'some_path')
        self.assertEqual(file_spec_set.audio_data, mock_audio_data_converted)
        self.assertAlmostEqual(file_spec_set.original_lufs, -15)
        self.assertEqual(file_spec_set.metadata, self.mock_metadata)
