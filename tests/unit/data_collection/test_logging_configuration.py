import unittest
import mock

from wavealign.data_collection.logging_configuration import (
    create_logging_config,
    setup_logging,
    output_logfile_warning,
)


class TestLoggingConfiguration(unittest.TestCase):
    @mock.patch("os.path.join", return_value="dummy_path")
    def test_create_logging_config(self, mock_os_path_join):
        output_path = "/path/to/directory"

        create_logging_config(output_path)

        mock_os_path_join.assert_called_once_with(output_path, "wavealign.log")

    @mock.patch("logging.config.dictConfig")
    @mock.patch("wavealign.data_collection.logging_configuration.create_logging_config")
    def test_setup_logging(self, mock_create_logging_config, mock_config_dictConfig):
        output_path = "/path/to/directory"
        setup_logging(output_path)
        mock_create_logging_config.assert_called_once_with(output_path)
        mock_config_dictConfig.assert_called_once_with(
            mock_create_logging_config.return_value
        )

    @mock.patch("os.path.join", return_value="dummy_path")
    @mock.patch("os.path.exists", return_value=True)
    def test_output_logfile_warning(self, mock_os_path_exists, mock_os_path_join):
        output_path = "/path/to/directory"

        with mock.patch("builtins.print") as mock_print:
            output_logfile_warning(output_path)

        mock_os_path_join.assert_called_once_with(output_path, "wavealign.log")
        mock_os_path_exists.assert_called_once_with("dummy_path")
        mock_print.assert_called_once_with(
            "\nSome files were not processed successfully. "
            "A log file at dummy_path was written."
        )
