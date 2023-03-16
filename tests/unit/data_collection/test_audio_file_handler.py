import mock
import unittest
from numpy import ndarray
from wavealign.data_collection.audio_file_spec_set import AudioFileSpecSet

from wavealign.data_collection.audio_file_handler import read, write

class TestAudioFileHandler(unittest.TestCase):
    
    @mock.patch('wavealign.data_collection.audio_file_handler.load_file')
    @mock.patch('wavealign.data_collection.audio_file_handler.soundfile.read')
    @mock.patch('wavealign.data_collection.audio_file_handler.calculate_lufs')
    def test_read(self, mock_calculate_lufs, mock_read, mock_load_file):
        
        fake_file_path = "/my/fake/dir/fake_file_1.wav"

        mock_load_file.return_value = {
                "not artwork": bytestream("this is not an artwork"),
                "artwork": bytestream("this is an artwork")
        }

        mock_read.return_value = ndarray, "44100"

        mock_calculate_lufs.return_value = 7.0

        expected_result = AudioFileSpecSet(
                file_path=fake_file_path,
                audio_data=ndarray,
                sample_rate=44100,
                artwork=bytestream("this is an artwork"),
                original_lufs=7.0
                )
       
        fake_output = read(fake_file_path)

        mock_load_file.assert_called_once_with(fake_file_path)
        mock_read.assert_called_once_with(fake_file_path)
        mock_calculate_lufs.assert_called_once_with(mock_read.return_value)


        self.assertEqual(fake_output, expected_result)
