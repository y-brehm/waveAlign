import unittest
from unittest import mock
import os

from wavealign.utility.logging.logger import Logger
from wavealign.utility.logging.warning_status_singleton import WarningStatusSingleton


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.mock_dictConfig = mock.patch(
            "wavealign.utility.logging.logger.dictConfig"
        ).start()
        self.mock_yaml_load = mock.patch("yaml.safe_load").start()
        self.mock_open = mock.patch("builtins.open", mock.mock_open(read_data="{}")).start()
        self.mock_os_path_dirname = mock.patch(
            "wavealign.utility.logging.logger.os.path.dirname",
            return_value=os.path.join("fake", "path"),
        ).start()
        self.mock_os_path_exists = mock.patch(
            "os.path.exists", return_value=True
        ).start()
        self.mock_print = mock.patch("builtins.print").start()
        self.output_path = os.path.join("fake", "path")
        self.verbose = True
        self.logger = Logger(self.output_path, self.verbose)

    def tearDown(self):
        mock.patch.stopall()

    def test_logger_initialization(self):
        self.mock_yaml_load.return_value = {
            "handlers": {"warning": {"filename": ""}, "debug": {"filename": ""}},
            "loggers": {"root": {"level": ""}},
        }

        expected_log_file_path = os.path.join("fake", "path", "wavealign.log")
        self.assertEqual(self.logger._Logger__log_file_path, expected_log_file_path)
        self.mock_open.assert_called_once_with(
            os.path.join("fake", "path", "logging_config.yaml"), "r"
        )
        self.mock_yaml_load.assert_called_once()
        self.mock_dictConfig.assert_called_once()

    def test_create_logging_config(self):
        self.mock_yaml_load.return_value = {
            "handlers": {"warning": {"filename": ""}, "debug": {"filename": ""}},
            "loggers": {"root": {"level": ""}},
        }
        config = self.logger._Logger__create_logging_config(
            self.output_path, self.verbose
        )

        expected_log_file_path = os.path.join(self.output_path, "wavealign.log")
        self.assertEqual(
            config["handlers"]["warning"]["filename"], expected_log_file_path
        )
        self.assertEqual(
            config["handlers"]["debug"]["filename"], expected_log_file_path
        )
        self.assertEqual(config["loggers"]["root"]["level"], "DEBUG")

    def test_output_logfile_warning_true(self):
        with mock.patch.object(
                WarningStatusSingleton, "get_warning_counts", return_value=True
        ):
            self.logger.output_logfile_warning()

        self.mock_os_path_exists.assert_called_once_with(
            os.path.join("fake", "path", "wavealign.log")
        )
        self.mock_print.assert_called_once_with(
            "\nSome files were not processed successfully. "
            f"A log file at {os.path.join('fake', 'path', 'wavealign.log')} was written."
        )

    def test_output_logfile_warning_false(self):
        with mock.patch.object(
                WarningStatusSingleton, "get_warning_counts", return_value=False
        ):
            self.logger.output_logfile_warning()

        self.mock_os_path_exists.assert_called_once_with(
            os.path.join("fake", "path", "wavealign.log")
        )
        self.mock_print.assert_not_called()
