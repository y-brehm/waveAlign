import unittest
import mock

from wavealign.utility.logging.warning_status_singleton import WarningStatusSingleton
from wavealign.utility.logging.output_logfile_warning import output_logfile_warning


class TestOutputLogfileWarning(unittest.TestCase):
    @mock.patch("os.path.join", return_value="dummy_path")
    @mock.patch("os.path.exists", return_value=True)
    @mock.patch("builtins.print")
    def test_output_logfile_warning_true(
        self,
        mock_print,
        mock_os_path_exists,
        mock_os_path_join,
    ):
        output_path = "/path/to/directory"
        with mock.patch.object(
            WarningStatusSingleton, "get_warning_counts", return_value=True
        ):
            output_logfile_warning(output_path)

        mock_os_path_join.assert_called_once_with(output_path, "wavealign.log")
        mock_os_path_exists.assert_called_once_with("dummy_path")
        mock_print.assert_called_once_with(
            "\nSome files were not processed successfully. "
            "A log file at dummy_path was written."
        )

    @mock.patch("os.path.join", return_value="dummy_path")
    @mock.patch("os.path.exists", return_value=True)
    @mock.patch("builtins.print")
    def test_output_logfile_warning_false(
        self,
        mock_print,
        mock_os_path_exists,
        mock_os_path_join,
    ):
        output_path = "/path/to/directory"
        with mock.patch.object(
            WarningStatusSingleton, "get_warning_counts", return_value=False
        ):
            output_logfile_warning(output_path)

        mock_os_path_join.assert_called_once_with(output_path, "wavealign.log")
        mock_os_path_exists.assert_called_once_with("dummy_path")
        mock_print.assert_not_called()
