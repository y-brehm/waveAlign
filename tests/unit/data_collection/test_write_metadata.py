import mock
import unittest

from src.wavealign.data_collection.write_metadata import write_metadata


@mock.patch('src.wavealign.data_collection.write_metadata.load_file')
class TestWriteMetadata(unittest.TestCase):
    def test_write_valid_metadata(self, mock_tag_load_file):
        mock_metadata = mock.MagicMock()
        mock_tag_load_file.return_value = mock_metadata

        write_metadata(mock.MagicMock(), 'some_path')

        mock_tag_load_file.assert_called_once_with('some_path')
        mock_metadata.save.assert_called_once()

    def test_write_faulty_metadata(self, mock_tag_load_file):
        mock_tag_load_file.return_value = None

        try:
            write_metadata(mock.MagicMock(), 'some_path')
        except ValueError:
            pass
        except Exception:
            self.fail('unexpected exception raised')
        else:
            self.fail('ExpectedException not raised')
