import logging


class WarningHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        global warning_counts
        if record.levelno == logging.WARNING:
            warning_counts = True
