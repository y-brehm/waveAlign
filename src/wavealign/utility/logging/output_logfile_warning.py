import os

from wavealign.utility.logging.logging_variables import LOGFILE_NAME, warning_counts


def output_logfile_warning(output_path: str) -> None:
    log_file_path = os.path.join(output_path, LOGFILE_NAME)

    if os.path.exists(log_file_path) and warning_counts:
        print(
            f"\nSome files were not processed successfully. "
            f"A log file at {log_file_path} was written."
        )