import unittest
import mock
import logging


from wavealign.utility.logging.warning_status_singleton import WarningStatusSingleton
from wavealign.utility.logging.handlers import WarningHandler


class TestWarningHandler(unittest.TestCase):
    def setUp(self):
        WarningStatusSingleton._instance = None
        self.logger = logging.getLogger("test_logger")
        self.logger.setLevel(logging.DEBUG)
        self.warning_handler = WarningHandler()
        self.logger.addHandler(self.warning_handler)

    def tearDown(self):
        self.logger.removeHandler(self.warning_handler)

    def test_emit_warning_log(self):
        with mock.patch.object(
            WarningStatusSingleton, "set_warning_counts"
        ) as mock_set_warning_counts:
            self.logger.warning("This is a warning")
            mock_set_warning_counts.assert_called_once()

    def test_emit_non_warning_log(self):
        with mock.patch.object(
            WarningStatusSingleton, "set_warning_counts"
        ) as mock_set_warning_counts:
            self.logger.info("This is an info message")
            mock_set_warning_counts.assert_not_called()
