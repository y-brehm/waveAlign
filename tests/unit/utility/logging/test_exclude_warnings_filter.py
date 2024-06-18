import unittest
import logging

from wavealign.utility.logging.exclude_warnings_filter import ExcludeWarningsFilter


class TestExcludeWarningsFilter(unittest.TestCase):
    def setUp(self):
        self.exclude_warnings_filter = ExcludeWarningsFilter()

    def test_filter_allows_lower_level_logs(self):
        debug_record = logging.LogRecord(
            name="test_logger",
            level=logging.DEBUG,
            pathname="",
            lineno=0,
            msg="This is a debug message",
            args=(),
            exc_info=None,
        )
        info_record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="This is an info message",
            args=(),
            exc_info=None,
        )

        self.assertTrue(self.exclude_warnings_filter.filter(debug_record))
        self.assertTrue(self.exclude_warnings_filter.filter(info_record))

    def test_filter_excludes_warning_and_higher_level_logs(self):
        warning_record = logging.LogRecord(
            name="test_logger",
            level=logging.WARNING,
            pathname="",
            lineno=0,
            msg="This is a warning message",
            args=(),
            exc_info=None,
        )
        error_record = logging.LogRecord(
            name="test_logger",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="This is an error message",
            args=(),
            exc_info=None,
        )
        critical_record = logging.LogRecord(
            name="test_logger",
            level=logging.CRITICAL,
            pathname="",
            lineno=0,
            msg="This is a critical message",
            args=(),
            exc_info=None,
        )

        self.assertFalse(self.exclude_warnings_filter.filter(warning_record))
        self.assertFalse(self.exclude_warnings_filter.filter(error_record))
        self.assertFalse(self.exclude_warnings_filter.filter(critical_record))
