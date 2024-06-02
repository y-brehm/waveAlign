import os
import logging.config


LOGFILE_NAME = "wavealign.log"
warning_counts = False


class WarningHandler(logging.Handler):
    def emit(self, record):
        global warning_counts
        if record.levelno == logging.WARNING:
            warning_counts = True


def create_logging_config(output_path: str) -> dict:
    log_file_path = os.path.join(output_path, LOGFILE_NAME)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "### %(name)s - %(message)s ###",
            },
            "logfile": {"format": "### %(asctime)s - %(name)s - %(message)s ###"},
        },
        "handlers": {
            "info": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
            "warning": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "WARNING",
                "formatter": "logfile",
                "filename": log_file_path,
                "maxBytes": 5000000,
                "backupCount": 3,
                "delay": True,
            },
            "warning_count": {
                "class": "wavealign.data_collection.logging_configuration.WarningHandler",
                "level": "WARNING",
            },
        },
        "loggers": {
            "root": {
                "level": "INFO",
                "handlers": ["info", "warning", "warning_count"],
            }
        },
    }

    return logging_config


def setup_logging(output_path: str) -> None:
    logging.config.dictConfig(create_logging_config(output_path))


def output_logfile_warning(output_path: str) -> None:
    log_file_path = os.path.join(output_path, LOGFILE_NAME)

    if os.path.exists(log_file_path) and warning_counts:
        print(
            f"\nSome files were not processed successfully. "
            f"A log file at {log_file_path} was written."
        )