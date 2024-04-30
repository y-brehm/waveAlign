import unittest
import mock

from wavealign.utility.ensure_path_exists import ensure_path_exists


class TestEnsurePathExists(unittest.TestCase):
    @mock.patch(
        "wavealign.utility.ensure_path_exists.os.path.exists", return_value=False
    )
    @mock.patch("wavealign.utility.ensure_path_exists.os.makedirs")
    def test_ensure_path_exists_not_exists(self, mock_makedirs, mock_exists):
        path = "/path/to/directory"
        ensure_path_exists(path)
        mock_exists.assert_called_once_with(path)
        mock_makedirs.assert_called_once_with(path)

    @mock.patch(
        "wavealign.utility.ensure_path_exists.os.path.exists", return_value=True
    )
    @mock.patch("wavealign.utility.ensure_path_exists.os.makedirs")
    def test_ensure_path_exists_already_exists(self, mock_makedirs, mock_exists):
        path = "/path/to/directory"
        ensure_path_exists(path)
        mock_exists.assert_called_once_with(path)
        mock_makedirs.assert_not_called()

    @mock.patch(
        "wavealign.utility.ensure_path_exists.os.path.exists", return_value=False
    )
    @mock.patch("wavealign.utility.ensure_path_exists.os.makedirs")
    def test_ensure_path_exists_empty_path(self, mock_makedirs, mock_exists):
        path = ""
        ensure_path_exists(path)
        mock_exists.assert_not_called()
        mock_makedirs.assert_not_called()
