import logging

from wavealign.utility.logging.warning_status_singleton import WarningStatusSigleton


class WarningHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno == logging.WARNING:
            warning_status = WarningStatusSigleton()
            warning_status.set_warning_counts()
