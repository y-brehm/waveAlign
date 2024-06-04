import logging.config

from wavealign.utility.logging.create_logging_config import create_logging_config


def setup_logging(output_path: str, verbose: bool) -> None:
    logging.config.dictConfig(create_logging_config(output_path, verbose))
