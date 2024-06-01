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
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            }
        },
        "handlers": {
            "skipped_files": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "clipped_files": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "WARNING",
                "formatter": "simple",
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

# don't use logging.info, but instead logger = logging.getLogger
# def setup_logging(output_path: str) -> logging.Logger:
#     logger = logging.getLogger("__name__")
#     logger.setLevel(logging.INFO)
#
#     file_handler = logging.FileHandler(log_file_path)
#     file_handler.setLevel(logging.INFO)
#
#     formatter = logging.Formatter(
#         "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#     )
#     file_handler.setFormatter(formatter)
#
#     logger.addHandler(file_handler)
#
#     return logger

def check_log_file() -> None:
    logger = logging.getLogger("__name__") #TODO: implementation
    if logger.hasHandlers() and logger.level > 0:
        print(
            f"Some files were not processed successfully. "
            f"Check the log file located at {logger.handlers[0].baseFilename} for details.")
