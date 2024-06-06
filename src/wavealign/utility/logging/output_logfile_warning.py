import os

from wavealign.utility.logging.create_logging_config import LOGFILE_NAME
from wavealign.utility.logging.warning_status_singleton import WarningStatusSingleton


def output_logfile_warning(output_path: str) -> None:
    log_file_path = os.path.join(output_path, LOGFILE_NAME)
    warning_status = WarningStatusSingleton()

    if os.path.exists(log_file_path) and warning_status.get_warning_counts():
        print(
            f"\nSome files were not processed successfully. "
            f"A log file at {log_file_path} was written."
        )
