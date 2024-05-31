import os
import time
import logging


def setup_logging(output_path: str) -> str:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_file_path = os.path.join(
        output_path,
        f"{timestamp}_wavealign.log",
    )

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return log_file_path

def write_log_file(output_path: str, problem_files: list[str]) -> None:
    log_file_path = setup_logging(output_path)
    logger = logging.getLogger(__name__)

    print(
        f"Some files were not processed successfully. "
        f"Check the log file located at {log_file_path} for details."
    )
    logger.info("The following files were not processed:")
    for problem_file in problem_files:
        logger.info(problem_file)
