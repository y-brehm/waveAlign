import os


LOGFILE_NAME = "wavealign.log"


def create_logging_config(output_path: str, verbose: bool) -> dict:
    log_file_path = os.path.join(output_path, LOGFILE_NAME)
    if verbose:
        log_level = "DEBUG"
    else:
        log_level = "INFO"

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {"format": "### %(name)s - %(message)s ###"},
            "logfile": {"format": "### %(asctime)s - %(name)s - %(message)s ###"},
            "debug": {"format": "### %(asctime)s - %(name)s - %(message)s ###"},
        },
        "filters": {
            "exclude_warnings": {
                "()": "wavealign.utility.logging.filters.ExcludeWarningsFilter",
            },
        },
        "handlers": {
            "info": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "console",
                "stream": "ext://sys.stdout",
                "filters": [],
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
                "class": "wavealign.utility.logging.handlers.WarningHandler",
                "level": "WARNING",
            },
            "debug": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "debug",
                "filename": log_file_path,
                "filters": ["exclude_warnings"],
            },
        },
        "loggers": {
            "root": {
                "level": log_level,
                "handlers": ["info", "warning", "warning_count", "debug"],
            }
        },
    }

    return logging_config
