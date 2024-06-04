import os
import logging.config


LOGFILE_NAME = "wavealign.log"
warning_counts = False


class WarningHandler(logging.Handler):
    def emit(self, record) -> None:
        global warning_counts
        if record.levelno == logging.WARNING:
            warning_counts = True


class ExcludeWarningsFilter(logging.Filter):
    def filter(self, record) -> bool:
        return record.levelno < logging.WARNING


def setup_logging(output_path: str, verbose: bool) -> None:
    logging.config.dictConfig(create_logging_config(output_path, verbose))


def output_logfile_warning(output_path: str) -> None:
    log_file_path = os.path.join(output_path, LOGFILE_NAME)

    if os.path.exists(log_file_path) and warning_counts:
        print(
            f"\nSome files were not processed successfully. "
            f"A log file at {log_file_path} was written."
        )
