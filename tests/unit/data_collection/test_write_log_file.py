import unittest
import mock
import logging

from wavealign.data_collection.write_log_file import (
    write_log_file,
)


class TestWriteLogFile(unittest.TestCase):
    @mock.patch("os.path.join", return_value="dummy_path")
    @mock.patch("time.strftime", return_value="dummy_timestamp")
    @mock.patch("logging.basicConfig")
    @mock.patch("logging.info")
    def test_write_log_file(
        self,
        mock_logging_info,
        mock_logging_basicConfig,
        mock_time_strftime,
        mock_os_path_join,
    ):
        problem_files = ["file1", "file2", "file3"]
        output_path = "/path/to/directory"

        with mock.patch("builtins.print") as mock_print:
            write_log_file(output_path, problem_files)

        mock_time_strftime.assert_called_once_with("%Y%m%d-%H%M%S")
        mock_os_path_join.assert_called_once_with(
            output_path, "dummy_timestamp_wavealign.log"
        )
        mock_logging_basicConfig.assert_called_once_with(
            filename="dummy_path", level=logging.INFO
        )
        mock_print.assert_called_once_with(
            "Some files were not processed successfully. "
            "Check the log file located at dummy_path for details."
        )
        mock_logging_info.assert_has_calls(
            [
                mock.call("The following files were not processed:"),
                mock.call("file1"),
                mock.call("file2"),
                mock.call("file3"),
            ]
        )
