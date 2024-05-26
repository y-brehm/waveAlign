import mock
import unittest

from mutagen import FileType
from wavealign.data_collection.write_metadata import write_metadata


@mock.patch("wavealign.data_collection.write_metadata.File")
class TestWriteMetadata(unittest.TestCase):
    def setUp(self):
        self.mock_audio_metadata = mock.MagicMock()

    def test_write_valid_metadata(self, mock_mutagen_file):
        mock_metadata = mock.MagicMock(spec=FileType)
        mock_mutagen_file.return_value = mock_metadata

        write_metadata("some_path", self.mock_audio_metadata)

        mock_mutagen_file.assert_called_once_with("some_path")
        mock_metadata.save.assert_called_once()

    def test_write_faulty_metadata(self, mock_mutagen_file):
        mock_mutagen_file.return_value = None

        with self.assertRaises(Exception):
            write_metadata("some_path", self.mock_audio_metadata)
