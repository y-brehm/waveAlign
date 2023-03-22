import mock
import unittest

from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet
from wavealign.data_collection.audio_file_handler import AudioFileHandler


class TestAudioFileHandler(unittest.TestCase):
    def setUp(self):
        self.fake_file_path = '/my/fake/dir/fake_file_1.wav'
        self.fake_artwork = bytearray([1, 2, 3, 4, 5])
        self.fake_audio_data = mock.MagicMock()
        self.fake_sample_rate = 44100
        self.fake_original_lufs = 7.0

    @mock.patch('wavealign.data_collection.audio_file_handler.load_file')
    @mock.patch('wavealign.data_collection.audio_file_handler.ffmpegio.audio.read')
    @mock.patch('wavealign.data_collection.audio_file_handler.calculate_lufs')
    def test_read(self, mock_calculate_lufs, mock_ffmpegio_read, mock_load_file):
        mock_load_file.return_value = {
                'no artwork': "test",
                'artwork': self.fake_artwork
                }
        mock_ffmpegio_read.return_value = (self.fake_sample_rate, self.fake_audio_data)
        mock_calculate_lufs.return_value = self.fake_original_lufs

        fake_output = AudioFileHandler().read(self.fake_file_path)

        self.assertIsInstance(fake_output, AudioFileSpecSet)
        self.assertEqual(fake_output.file_path, self.fake_file_path)
        self.assertEqual(fake_output.audio_data, self.fake_audio_data)
        self.assertEqual(fake_output.sample_rate, self.fake_sample_rate)
        self.assertEqual(fake_output.artwork, self.fake_artwork)
        self.assertEqual(fake_output.original_lufs, self.fake_original_lufs)

        mock_load_file.assert_called_once_with(self.fake_file_path)
        mock_ffmpegio_read.assert_called_once_with(self.fake_file_path)
        mock_calculate_lufs.assert_called_once_with(self.fake_audio_data, self.fake_sample_rate)

    @mock.patch('wavealign.data_collection.audio_file_handler.ffmpegio.audio.write')
    @mock.patch('wavealign.data_collection.audio_file_handler.load_file')
    def test_write(self, mock_load_file, mock_ffmpegio_write):
        fake_audio_file_spec_set = AudioFileSpecSet(
                file_path=self.fake_file_path,
                audio_data=self.fake_audio_data,
                original_lufs=self.fake_original_lufs,
                sample_rate=self.fake_sample_rate,
                artwork=self.fake_artwork,
                )

        AudioFileHandler().write(self.fake_file_path, fake_audio_file_spec_set)

        mock_ffmpegio_write.assert_called_once_with(
                self.fake_file_path,
                self.fake_sample_rate,
                self.fake_audio_data,
                )

        mock_load_file.assert_called_once_with(self.fake_file_path)
        mock_load_file.return_value.__setitem__\
            .assert_called_once_with('artwork', fake_audio_file_spec_set.artwork)
        mock_load_file.return_value.save.assert_called_once()
