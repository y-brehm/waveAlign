import mock
import unittest

from wavealign.data_collection.metadata_extractor import MetaDataExtractor
from wavealign.data_collection.audio_metadata import AudioMetadata


class TestMetadataExtractor(unittest.TestCase):
    def setUp(self):
        self.mock_metadata = mock.MagicMock()
        self.mock_details = {
            "streams": [
                {
                    "channels": 2,
                    "codec_name": "eva02",
                    "sample_rate": 44100,
                    "bit_rate": 16000,
                }
            ],
        }

        self.mock_probe_details = mock.patch(
            "wavealign.data_collection.metadata_extractor.probe.full_details"
        ).start()
        self.mock_mutagen_file = mock.patch(
            "wavealign.data_collection.metadata_extractor.File"
        ).start()

        self.mock_mutagen_file.return_value = self.mock_metadata
        self.mock_probe_details.return_value = self.mock_details

    def tearDown(self):
        mock.patch.stopall()

    def test_extract(self):
        metadata = MetaDataExtractor().extract("some_path")

        expect = AudioMetadata(
            num_channels=2,
            metadata=self.mock_metadata,
            codec_name="eva02",
            bit_rate="16k",
            sample_rate=44100,
        )
        self.assertEqual(expect.__repr__(), metadata.__repr__())
