import unittest
import mock

import numpy as np

from wavealign.data_collection.audio_file_reader import AudioFileReader


class TestAudioFileReader(unittest.TestCase):
    def setUp(self):
        self.mock_audio_read = mock.patch(
            "wavealign.data_collection.audio_file_reader.audio.read"
        ).start()
        self.mock_pcm_float_converter = mock.patch(
            "wavealign.data_collection.audio_file_reader.PcmFloatConverter"
        ).start()
        self.__fake_audio_read_return = (
            48000,
            np.array([0, 32767, -32768], dtype=np.int16),
        )
        self.mock_audio_read.return_value = self.__fake_audio_read_return

    def tearDown(self):
        mock.patch.stopall()

    def test_read_pcm_encoded(self):
        self.mock_pcm_float_converter.is_pcm_encoded.return_value = True
        fake_pcm_to_float_return = np.array([0.0, 1.0, -1.0], dtype=np.float32)
        self.mock_pcm_float_converter.return_value.pcm_to_float.return_value = (
            fake_pcm_to_float_return
        )

        reader = AudioFileReader()
        audio_data = reader.read("dummy_path")

        self.mock_audio_read.assert_called_once_with("dummy_path")
        self.mock_pcm_float_converter.return_value.is_pcm_encoded.assert_called_once_with(
            self.__fake_audio_read_return[1]
        )
        self.mock_pcm_float_converter.return_value.pcm_to_float.assert_called_once_with(
            self.__fake_audio_read_return[1]
        )
        np.testing.assert_array_almost_equal(
            audio_data, fake_pcm_to_float_return, decimal=4
        )

    def test_read_not_pcm_encoded(self):
        self.mock_pcm_float_converter.return_value.is_pcm_encoded.return_value = False

        reader = AudioFileReader()
        audio_data = reader.read("dummy_path")

        self.mock_audio_read.assert_called_once_with("dummy_path")
        self.mock_pcm_float_converter.return_value.is_pcm_encoded.assert_called_once_with(
            self.__fake_audio_read_return[1]
        )
        self.mock_pcm_float_converter.return_value.pcm_to_float.assert_not_called()
        np.testing.assert_array_almost_equal(
            audio_data, self.__fake_audio_read_return[1], decimal=4
        )
