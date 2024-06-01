import os
import time
import logging.config

def create_logging_config(output_path: str) -> dict:
    log_file_path = os.path.join(
        output_path,
        "wavealign.log",
    )

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "### %(name)s - %(message)s ###",
            },
            "logfile": {
                "format": "### %(asctime)s - %(name)s - %(message)s ###"
            }

        },
        "handlers": {
            "skipped_files": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
            "clipped_files": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "WARNING",
                "formatter": "logfile",
                "filename": log_file_path,
                "maxBytes": 5000000,
                "backupCount": 3,
            }
        },
        "loggers": {
            "root": {
                "level": "INFO",
                "handlers": [
                    "skipped_files", 
                    "clipped_files"
                ],
            }
        },
    }

    return logging_config

def setup_logging(output_path: str) -> None:
    
    logging.config.dictConfig(create_logging_config(output_path))

def check_log_file() -> None:
    logger = logging.getLogger("__name__") #TODO: implementation
    if logger.hasHandlers() and logger.level > 0:
        print(
            f"Some files were not processed successfully. "
            f"Check the log file located at {logger.handlers[0].baseFilename} for details.")
