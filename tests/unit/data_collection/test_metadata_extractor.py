import mock
import unittest

from wavealign.data_collection.metadata_extractor import MetaDataExtractor
from wavealign.data_collection.audio_metadata import AudioMetadata


class TestMetadataExtractor(unittest.TestCase):
    def setUp(self):
        self.mock_artwork = mock.MagicMock()
        self.mock_tag_metadata = {
                'artwork': self.mock_artwork
                }
        self.mock_details = {
                'streams': [{
                    'channels': 2,
                    'codec_name': 'eva02',
                    'sample_rate': 44100,
                    'bit_rate': 16000,
                    }],
        }

        self.mock_probe_details = mock.patch(
            'wavealign.data_collection.metadata_extractor.probe.full_details').start()
        self.mock_tag_load_file = mock.patch(
            'wavealign.data_collection.metadata_extractor.load_file').start()

        self.mock_tag_load_file.return_value = self.mock_tag_metadata
        self.mock_probe_details.return_value = self.mock_details

    def tearDown(self):
        mock.patch.stopall()

    def test_extract(self):
        metadata = MetaDataExtractor().extract('some_path')

        expect = AudioMetadata(
            num_channels=2,
            artwork=self.mock_artwork,
            codec_name='eva02',
            bit_rate='16k',
            sample_rate=44100
           )
        self.assertEqual(expect.__repr__(), metadata.__repr__())


class TestMetadataExtractorAssert(unittest.TestCase):
    @mock.patch('wavealign.data_collection.metadata_extractor.load_file')
    def test_write_with_faulty_metadata(self, mock_tag_load_file):
        mock_tag_load_file.return_value = None

        try:
            MetaDataExtractor().extract('some_path')
        except Exception as e:
            if "Failed to read metadata for" not in str(e):
                self.fail('unexpected exception raised')
        else:
            self.fail('ExpectedException not raised')
