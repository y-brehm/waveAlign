import mock
import unittest

from wavealign.data_collection.write_metadata import write_metadata


@mock.patch("wavealign.data_collection.write_metadata.load_file")
class TestWriteMetadata(unittest.TestCase):
    def setUp(self):
        self.mock_audio_metadata = mock.MagicMock()

    def test_write_valid_metadata(self, mock_tag_load_file):
        mock_metadata = mock.MagicMock()
        mock_tag_load_file.return_value = mock_metadata

        write_metadata("some_path", self.mock_audio_metadata)

        mock_tag_load_file.assert_called_once_with("some_path")
        mock_metadata.save.assert_called_once()

    def test_write_faulty_metadata(self, mock_tag_load_file):
        mock_tag_load_file.return_value = None

        with self.assertRaises(Exception):
            write_metadata("some_path", self.mock_audio_metadata)
