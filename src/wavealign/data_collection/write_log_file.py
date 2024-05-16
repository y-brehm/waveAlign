import os
import time
import logging

# TODO: check logging framework for better implementation than this #28


def write_log_file(output_path: str, problem_files: list[str]) -> None:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_file_path = os.path.join(
        output_path,
        f"{timestamp}_wavealign.log",
    )

    logging.basicConfig(filename=log_file_path, level=logging.INFO)
    print(
        f"Some files were not processed successfully. "
        f"Check the log file located at {log_file_path} for details."
    )
    logging.info("The following files were not processed:")
    for problem_file in problem_files:
        logging.info(problem_file)
