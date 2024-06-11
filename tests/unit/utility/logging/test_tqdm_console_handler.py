from logging import LogRecord
import unittest
import mock

from wavealign.utility.logging.tqdm_console_handler import TqdmConsoleHandler


class TestTqdmConsoleHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = TqdmConsoleHandler()
        self.record = LogRecord(
            name="test",
            level=20,
            pathname="",
            lineno=0,
            msg="Test Message",
            args=(),
            exc_info=None,
        )

    @mock.patch("wavealign.utility.logging.tqdm_console_handler.tqdm.write")
    def test_emit_writes_messages(self, mock_tqdm_write):
        self.handler.emit(self.record)
        mock_tqdm_write.assert_called_once_with("Test Message")

    @mock.patch("wavealign.utility.logging.tqdm_console_handler.tqdm.write")
    def test_emit_handles_exception(self, mock_tqdm_write):
        self.handler.format = mock.Mock(side_effect=Exception("formatting error"))

        with mock.patch.object(self.handler, "handleError") as mock_handle_error:
            self.handler.emit(self.record)
            mock_handle_error.assert_called_once_with(self.record)
        mock_tqdm_write.assert_not_called()
