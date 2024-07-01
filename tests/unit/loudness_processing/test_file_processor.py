import mock
import unittest
import numpy as np

from wavealign.data_collection.audio_metadata import AudioMetadata
from wavealign.data_collection.audio_property_set import AudioPropertySet
from wavealign.loudness_processing.audio_file_processor import AudioFileProcessor


class TestAudioFileProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_compressed_file_processor = mock.patch(
            "wavealign.loudness_processing.audio_file_processor.CompressedFileProcessor"
        ).start()
        self.mock_uncompressed_file_processor = mock.patch(
            "wavealign.loudness_processing.audio_file_processor.UncompressedFileProcessor"
        ).start()
        self.audio_property_set = AudioPropertySet(
            file_path="file1.wav",
            last_modified=1234,
            original_peak_level=-1,
            original_lufs_level=-14,
            metadata=AudioMetadata(
                num_channels=1,
                metadata=mock.MagicMock(),
                codec_name="aiff",
                bit_rate="128000",
                sample_rate=44100,
            ),
        )
        self.target_level = -10
        self.output_file_path = "output.mp3"
        self.audio_data = np.array([1, 2, 3])

    def tearDown(self):
        mock.patch.stopall()

    def test_calls_uncompressed_file_processor(self):
        AudioFileProcessor().process(
            self.audio_property_set,
            self.target_level,
            self.output_file_path,
            self.audio_data,
        )

        self.mock_uncompressed_file_processor.return_value.process.assert_called_once_with(
            self.audio_property_set,
            self.target_level,
            self.output_file_path,
            self.audio_data,
        )
        self.mock_compressed_file_processor.return_value.process.assert_not_called()

    def test_calls_compressed_file_processor(self):
        self.audio_property_set.metadata.codec_name = "mp3"
        print(self.audio_property_set.metadata.codec_name)
        AudioFileProcessor().process(
            self.audio_property_set,
            self.target_level,
            self.output_file_path,
            self.audio_data,
        )

        self.mock_compressed_file_processor.return_value.process.assert_called_once_with(
            self.audio_property_set, self.target_level, self.output_file_path
        )
        self.mock_uncompressed_file_processor.return_value.process.assert_not_called()
